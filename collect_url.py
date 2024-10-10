from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
from datetime import datetime
import time

def initialize_browser():
    options = Options()
    options.add_argument("--disable-extensions")
    options.headless = False
    return webdriver.Chrome(options=options)


def wait_for_element(driver, by, value, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def main():
    driver_path = 'chromedriver'
    browser = initialize_browser()

    try:
        url = "https://www.fishbowlapp.com/bowl/the-work-life-bowl"
        browser.get(url)

        cookies = {
            "name": 'session_key',
            "value": 'b5e39981-f633-4819-b54b-9afdde740e73'
        }

        browser.add_cookie(cookies)
        browser.refresh()

        with open('anxiety_data.csv', 'r') as csvfile, open('anxiety_posts_V1.csv', 'w', newline='', encoding='utf-8') as post_data_file,open('anxiety_comments_V1.csv', 'w', newline='', encoding='utf-8') as comment_data_file:
            reader = csv.DictReader(csvfile)
            fieldnames = ['Neurodiversity', 'Posted By', 'Employer', 'Post Type', 'Time Posted', 'Content', 'Likes', 'Comments', 'Shares', 'Timestamp Collected', 'Post URL', 'Post ID']
            writer = csv.DictWriter(post_data_file, fieldnames=fieldnames)
            writer.writeheader()

            comment_fieldnames = ['Neurodiversity', 'Posted By', 'Employer', 'Time Posted', 'Content', 'Reactions', 'Timestamp Collected', 'Post URL','Hierarchy', 'Post ID', 'Comment ID']
            comments_writer = csv.DictWriter(comment_data_file, fieldnames=comment_fieldnames)
            comments_writer.writeheader()

            
            comment_id=1
            counter=0 
            startup_index=600 #change based on starting index
            for row in reader:
                counter+=1
                print(f"COUNTER: {counter}")
                if counter>=startup_index:
                    post_url = row['post_urls']
                    post_id = row['id']
                    print(f"Processing URL: {post_url}")

                    browser.set_page_load_timeout(60)
                    browser.get(post_url)
                    #time.sleep(2)

                    post_data = {}
                    post_data['Neurodiversity'] = 'Anxiety'
                    post_data['Post URL'] = post_url
                    post_data['Post ID'] = post_id
                    post_data['Timestamp Collected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    comment_bool=False
                    try:

                        comment_elements = browser.find_element(By.CSS_SELECTOR, "div.row.comments-list")
                        comments = comment_elements.find_elements(By.CSS_SELECTOR, 'app-post.comment')
                        comment_bool=True

                    except:
                        print('No comments found')

                    while True:
                        try:
                            view_more_button = WebDriverWait(browser, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.view-more")))
                            view_more_button.click()
                            
                            time.sleep(5)  
                            
                        except:
                            
                            print("All replies have been loaded.")
                            break
                    
                    if comment_bool:
                        for comment in comments:
                            reply_counter=1
                            comment_data = {}
                            comment_data['Neurodiversity'] = 'Anxiety'
                            comment_data['Hierarchy'] = 1
                            comment_data['Post URL'] = post_url
                            comment_data['Post ID'] = post_id
                            comment_data['Comment ID'] = comment_id
                            comment_data['Timestamp Collected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        

                            try:
                                comment_data['Content'] = comment.find_element(By.XPATH, './/h2[contains(@class, "post-text")]').text
                        
                            except:
                                try:
                                    comment_data['Content'] = comment.find_element(By.XPATH, './/p[contains(@class, "post-text")]').text
                                except:
                                    comment_data['Content'] = ''
                                    comment_html = comment.get_attribute('outerHTML') #used for troubleshooting because not all comments get collected using the XPATHS above
                                    print("Comment HTML: ", comment_html,'\n')

                            try:
                                comment_data['Employer'] = comment.find_element(By.CSS_SELECTOR, 'div.post-author div.header div.work-title').text

                            except:
                                try:
                                    comment_data['Employer'] = comment.find_element(By.CSS_SELECTOR, 'div.work.step.title > span:not(.preposition)').text
                                except:
                                    try:
                                        comment_data['Employer'] = comment.find_element(By.CSS_SELECTOR, "div.post-author div.header div.work span.ng-star-inserted").text
                                        
                                    except:
                                        try:
                                            comment_data['Employer'] = comment.find_element(By.CSS_SELECTOR, "div.work-title span.preposition + span.ng-star-inserted").text
                                        except Exception as e:
                                            comment_data['Employer'] = ''
                                            #comment_html = comment.get_attribute('outerHTML') #used for troubleshooting
                                            #print("Employer HTML: ", comment_html,'\n')
                                            print("Error extracting employer:", str(e))
                                            

                            try:
                                comment_data['Time Posted'] = comment.find_element(By.CSS_SELECTOR, 'app-post.comment.ng-star-inserted div.post-actions span.time').text
                            except:
                                comment_data['Time Posted'] = ''
                            
                            try:
                                reactions_text = comment.find_element(By.CSS_SELECTOR, 'app-post.comment.ng-star-inserted div.post-actions span.likes').text
                                comment_data['Reactions'] = reactions_text.split()[0]
                            except:
                                comment_data['Reactions'] = ''

                            try:
                                author_badge = reply.find_element(By.CSS_SELECTOR, 'author-badge')
                                comment_data['Posted By'] = 'Author'
                            except:
                                comment_data['Posted By'] = 'Other'


                            comments_writer.writerow(comment_data)
                            #print('Comment data:', comment_data)

                            comment_data_file.flush()
                            
                        
                            
                            comment_id+=1
                            #replies = comment.find_elements(By.CSS_SELECTOR, 'app-post.comment.ng-star-inserted div.comments-replies.show-more')
                            replies = comment.find_elements(By.CSS_SELECTOR, 'app-post.comment-reply.comment')
                            
                            for reply in replies:
                                reply_counter+=1
                                comment_data['Neurodiversity'] = 'Anxiety'
                                comment_data['Hierarchy'] = reply_counter
                                comment_data['Post URL'] = post_url
                                comment_data['Post ID'] = post_id
                                comment_data['Comment ID'] = comment_id
                                comment_data['Timestamp Collected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                try:
                                    comment_data['Content'] = reply.find_element(By.CSS_SELECTOR, 'p.post-text.type-text').text
                                except:
                                    comment_data['Content'] = ''

                                try:
                                    comment_data['Employer'] = reply.find_element(By.CSS_SELECTOR, 'div.work-title, div.company.type').text
                                except:
                                    comment_data['Employer'] = ''

                                try: 
                                    comment_data['Reactions'] = reply.find_element(By.CSS_SELECTOR, 'reactions-counter span.likes').text
                                except:
                                    comment_data['Reactions'] = ''

                                try: 
                                    comment_data['Time Posted'] = reply.find_element(By.CSS_SELECTOR, 'span.time').text
                                except:
                                    comment_data['Time Posted'] = ''

                                try:
                                    author_badge = reply.find_element(By.CSS_SELECTOR, 'author-badge')
                                    comment_data['Posted By'] = 'Author'
                                except:
                                    comment_data['Posted By'] = 'Other'

                                comments_writer.writerow(comment_data)
                                #print('Reply data:', comment_data)

                                comment_data_file.flush()
                                comment_id+=1


                    try:
                        posted_by_element = wait_for_element(browser, By.CSS_SELECTOR, "div.work-title.step.title")
                        post_data['Posted By'] = posted_by_element.text
                    except:
                        post_data['Posted By'] = ''

                    try:
                        #work_at_element = wait_for_element(browser, By.CSS_SELECTOR, "div.work.step.title")
                        work_at_element = wait_for_element(browser, By.CSS_SELECTOR, "div.work.step.title > span:nth-of-type(2)")
                        post_data['Employer'] = work_at_element.text
                    except:
                        post_data['Employer'] = ''

                    try:
                        post_type_element = wait_for_element(browser, By.CSS_SELECTOR, "span.bowl-title")
                        post_data['Post Type'] = post_type_element.text
                    except:
                        post_data['Post Type'] = ''

                    try:
                        time_posted_element = wait_for_element(browser, By.CSS_SELECTOR, "div.post-time")
                        post_data['Time Posted'] = time_posted_element.text
                    except:
                        post_data['Time Posted'] = ''

                    try:
                        content_element = wait_for_element(browser, By.CSS_SELECTOR, ".post-text.type-text.ng-star-inserted")
                        text_content = content_element.text
                        for child_element in content_element.find_elements(By.CSS_SELECTOR, "div.likes.ng-star-inserted"):
                            text_content = text_content.replace(child_element.text, '')
                        post_data['Content'] = text_content
                    except:
                        post_data['Content'] = ''

                    try:
                        likes_element = wait_for_element(browser, By.CSS_SELECTOR, "span.likes.ng-star-inserted")
                        likes = likes_element.text.strip()
                        if "reactions" in likes.lower():
                            likes = likes.split()[0]
                        post_data['Likes'] = likes
                    except:
                        post_data['Likes'] = ''

                    try:
                        comments_element = wait_for_element(browser, By.CSS_SELECTOR,"button.action.comment.ng-star-inserted")
                        post_data['Comments'] = ''.join(filter(str.isdigit, comments_element.text))
                    except:
                        post_data['Comments'] = ''

                    try:
                        shares_element = wait_for_element(browser, By.CSS_SELECTOR, "span.share-counter.ng-star-inserted")
                        post_data['Shares'] = shares_element.text
                    except:
                        post_data['Shares'] = ''


                    writer.writerow(post_data)
                    #print('Post data:', post_data)

                    post_data_file.flush()  # Flush the buffer to immediately write to the file
                    # post_id+=1

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        browser.quit()

if __name__ == "__main__":
    main()

