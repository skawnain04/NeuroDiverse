#Data pre-processing
import pandas as pd

#open AI
import openai
from openai import AzureOpenAI

# Set up your Azure OpenAI credentials
AZURE_OPENAI_ENDPOINT = "https://benchchat.openai.azure.com/"
AZURE_OPENAI_API_KEY = "28b301cb28c347ca8714129af7dc9416"

client = AzureOpenAI(
  azure_endpoint = AZURE_OPENAI_ENDPOINT,
  api_key=AZURE_OPENAI_API_KEY,
  api_version="2024-02-01"
)

path = 'Data/all_comments.csv'
df_org = pd.read_csv(path)
print(df_org.count())

#removing NAN
df = df_org.dropna(subset=['Content'])
print(df.count())

#Prompts

# Define the function to check if a question is related what kind of Neuro Disease
def related_diseases(question):

    messages = [
    {"role": "system", "content": "You are an expert assistant specialized in recognizing NeuroDiverse conditions."},
    {"role": "user", "content": f"""Based on the following context, identify the NeuroDiverse condition it relates to. Your answer should be limited to one of these conditions: ADHD, Anxiety, Autism, Bipolar Disorder (BPD), Borderline Personality Disorder (BPD), Depression, Dyslexia, Obsessive-Compulsive Disorder (OCD), Post-Traumatic Stress Disorder (PTSD), or Schizophrenia.

    Provide your answer as one word corresponding to the correct condition from the list above.

    Question: \"{question}\"

    Answer:"""}
    ]

    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=2,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            # Check if answer is one of the allowed diseases, otherwise return "Unknown"
            allowed_diseases = ["ADHD", "Anxiety", "Autism", "Bipolar", "BPD", "Depression", "Dyslexia", "OCD", "PTSD", "Schizophrenia"]
            if answer not in allowed_diseases:
              answer = "Unknown" # Assign "Unknown" if the answer is not in allowed diseases
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"

# Contains medical advice
# Define the function to check if a question is related what kind of Neuro Disease
def medical_advice(question):
    # Construct the messages for the chat completion
    # v1
    messages = [
    {"role": "system", "content": """You are an AI assistant trained to detect medical advice or information in forum posts. Your task is to determine if the given text provides any form of medical guidance, advice, or information.

    Medical advice or information includes, but is not limited to:
    1. Suggestions for diagnosing or treating medical conditions
    2. Explanations or descriptions of medical procedures or treatments
    3. Interpretations of medical symptoms, conditions, or test results
    4. Recommendations for managing or improving health conditions

    Respond with 'Yes' if any part of the text contains medical advice or information. Respond with 'No' if it does not."""},

        {"role": "user", "content": f"""Examine the following forum content and determine if it contains any medical advice or information as described in the system instructions.
    Respond with ONLY 'Yes' or 'No'.

    Forum Content: "{question}"

    Provide your answer in one word only:"""}
    ]



    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"

# Topic identification
def which_topic(question):
    # Construct the messages for the chat completion
    messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"""Analyze the following question and identify the main topic it addresses. Provide your answer with a keyword or phrase in 4 words or less.\n\nQuestion: \"{question}\"\n\nAnswer:"""}
    ]


    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"
    
# Define the function to check if a question is related to workplace difficulties
def is_related_to_workplace(question):

    messages = [
        {"role": "system", "content": """You are an AI assistant specialized in analyzing text for workplace-related content. Your task is to determine if a given text pertains to any aspect of professional life or work environments, including but not limited to:

    1. Job responsibilities and tasks
    2. Workplace relationships and interactions
    3. Professional development and career growth
    4. Company culture and organizational structure
    5. Work-life balance
    6. Office or remote work environments
    7. Business processes and operations
    8. Professional communication
    9. Workplace policies and procedures
    10. Industry-specific topics in a professional context
    11. Job satisfaction or dissatisfaction
    12. Workplace challenges or successes
    13. Professional goals and aspirations
    14. Work-related tools, technologies, or equipment
    15. Business strategies or decision-making

    The text does not need to be about difficulties or problems to be considered workplace-related.

    Respond with a single word: 'Yes' if the text relates to any workplace or professional topic, or 'No' if it does not."""},

        {"role": "user", "content": f"""Analyze the following text and determine if it pertains to any workplace or professional context as described above.

    Text: "{question}"

    Provide your answer in one word only:"""}
    ]

    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"

# Define the function to check if a question is Detecting Medical and Medication-Related Queries
def medical_medicine_related(question):
    
    messages = [
        {"role": "system", "content": """You are an AI assistant specialized in analyzing forum content. 
      Your task is to determine if a given text contains:
      1. Requests for medical advice
      2. Questions about medication management
      3. Inquiries about drug interactions, side effects, or dosage
      4. Requests for diagnosis or treatment recommendations

      Respond with 'Yes' if ANY of these are present, and 'No' otherwise."""},
              {"role": "user", "content": f"""Analyze the following forum content and determine if it contains any requests for medical advice, medication information, or related health queries as described in the system message. 
      Respond with ONLY 'Yes' or 'No'.

      Forum Content: "{question}"

      Provide your answer in one word only:"""}
    ]


    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"
    
# Does the post contains medical advice
def medicine_related_content(question):
    # Construct the messages for the chat completion
    # v1
    messages = [
    {"role": "system", "content": """You are an AI assistant trained to detect medicine-related content in forum posts. Your task is to determine if the given text contains any information about medicines, drugs, or pharmaceutical products.

    Medicine-related content includes, but is not limited to:
    1. Mentions of specific medication names (generic or brand names)
    2. Information about drug dosages, side effects, or interactions
    3. Discussions about over-the-counter or prescription medications
    4. Questions or comments about the use of pharmaceutical products

    Respond with 'Yes' if any part of the text contains medicine-related content. Respond with 'No' if it does not."""},

        {"role": "user", "content": f"""Examine the following forum content and determine if it contains any medicine-related content as described in the system instructions.
    Respond with ONLY 'Yes' or 'No'.

    Forum Content: "{question}"

    Provide your answer in one word only:"""}
    ]



    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"

# Discrimination detection
def discrimination(question):
    # Construct the messages for the chat completion
    messages = [
    {"role": "system", "content": """You are an AI assistant specialized in analyzing text for discriminatory content related to neurodiverse disabilities and mental health conditions. Your task is to determine if a given text contains any form of discrimination specifically targeting individuals with neurodiverse or mental health conditions, which may include but is not limited to:

      1. Discrimination based on neurodiverse conditions such as autism spectrum disorders (ASD), ADHD, dyslexia, dysgraphia, or Tourette syndrome
      2. Discrimination based on mental health conditions such as:
          - Bipolar disorder
          - Anxiety disorders
          - Borderline personality disorder (BPD)
          - Depression
          - Obsessive-compulsive disorder (OCD)
          - Post-traumatic stress disorder (PTSD)
          - Schizophrenia or other psychotic disorders
      3. Any form of biased treatment, exclusion, derogatory statements, or negative assumptions aimed at individuals based on their neurodiverse or mental health conditions
      4. Stereotyping, belittling, or making harmful assumptions about someone's abilities, intelligence, behavior, or worth based on these conditions

      Discrimination may include unfair treatment, derogatory comments, exclusion, stereotyping, or assumptions about capability or character due to neurodiversity or mental health conditions.

      Respond with 'Yes' if the content contains any form of discrimination based on neurodiverse disabilities or mental health conditions, and 'No' if it does not."""},

          {"role": "user", "content": f"""Analyze the following text and determine if it contains any form of discrimination based on neurodiverse disabilities or mental health conditions as described above.

      Text: "{question}"

      Provide your answer in one word only:"""}
      ]



    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"
    
# personal relational challenges detection
def relational_challenges(question):
    # Construct the messages for the chat completion
    messages = [
    {"role": "system", "content": """You are an AI assistant specialized in analyzing text for personal relationship challenges specifically related to neurological diseases (Bipolar disorder, Anxiety disorders, Borderline personality disorder (BPD), Depression, Obsessive-compulsive disorder (OCD), Post-traumatic stress disorder (PTSD), ADHD, Autism spectrum disorders, Schizophrenia or other psychotic disorders). Your task is to determine if the given text discusses or implies any form of relationship difficulties directly caused by these neurological conditions

      

      Focus on identifying relationship problems such as:

      - Communication difficulties due to the cognitive or emotional effects of these conditions on personal relations
      - Emotional distance, disconnection, or personality changes that strain personal relationships
      - Stress or frustration from caregiving responsibilities related to the condition
      - Intimacy issues resulting from the physical or psychological effects of the condition
      - Misunderstandings or arguments resulting from symptoms like memory loss, anxiety, or mood swings that can affect personal relationships
      - Resentment or frustration from either partner because of the challenges posed by the condition
      - Difficulty maintaining friendships or social connections due to the neurological disease

      Respond with 'Yes' if the content explicitly mentions or strongly implies relationship challenges directly related to the neurological diseases listed above. Respond with 'No' if it does not, or if the diseases are mentioned without clear reference to relationship issues."""},

          {"role": "user", "content": f"""Analyze the following text and determine if it contains any mention of personal relationship challenges specifically due to neurological diseases as described above.

      Text: "{question}"

      Provide your answer in one word only:"""}
      ]





    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"
    
# Discrimination detection
def social_emotional_challenges(question):
    # Construct the messages for the chat completion
    messages = [
    {"role": "system", "content": """You are an AI assistant specialized in analyzing text for discriminatory content related to neurodiverse disabilities and mental health conditions. Your task is to determine if a given text contains any form of discrimination specifically targeting individuals with neurodiverse or mental health conditions, which may include but is not limited to:

      1. Discrimination based on neurodiverse conditions such as autism spectrum disorders (ASD), ADHD, dyslexia, dysgraphia, or Tourette syndrome
      2. Discrimination based on mental health conditions such as:
          - Bipolar disorder
          - Anxiety disorders
          - Borderline personality disorder (BPD)
          - Depression
          - Obsessive-compulsive disorder (OCD)
          - Post-traumatic stress disorder (PTSD)
          - Schizophrenia or other psychotic disorders
      3. Any form of biased treatment, exclusion, derogatory statements, or negative assumptions aimed at individuals based on their neurodiverse or mental health conditions
      4. Stereotyping, belittling, or making harmful assumptions about someone's abilities, intelligence, behavior, or worth based on these conditions

      Discrimination may include unfair treatment, derogatory comments, exclusion, stereotyping, or assumptions about capability or character due to neurodiversity or mental health conditions.

      Respond with 'Yes' if the content contains any form of discrimination based on neurodiverse disabilities or mental health conditions, and 'No' if it does not."""},

          {"role": "user", "content": f"""Analyze the following text and determine if it contains any form of discrimination based on neurodiverse disabilities or mental health conditions as described above.

      Text: "{question}"

      Provide your answer in one word only:"""}
      ]



    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip() # Extract the answer from the message content
            return answer
        else:
          print(f"Empty response for question: {question}")
          return "None"

        answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
        return answer

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Unknown' or handle the error in another way
        return "Problematic"

# Managing_diseases
def managing_diseases(question):
    # Construct the messages for the chat completion
    messages = [
        {"role": "system", "content": """You are an AI assistant specialized in analyzing text for information related to managing neurological diseases. Your task is to determine if the given text discusses or implies any methods, strategies, or advice for managing neurological conditions, including but not limited to:

        1. Bipolar disorder
        2. Anxiety disorders
        3. Borderline personality disorder (BPD)
        4. Depression
        5. Obsessive-compulsive disorder (OCD)
        6. Post-traumatic stress disorder (PTSD)
        7. ADHD
        8. Autism spectrum disorders
        9. Schizophrenia or other psychotic disorders

        Focus on identifying management strategies such as:

        - Medication usage, dosage, or adjustments to treat symptoms
        - Therapy or counseling options (e.g., cognitive-behavioral therapy, talk therapy)
        - Coping mechanisms or techniques to manage symptoms in daily life
        - Lifestyle changes (e.g., diet, exercise, sleep habits) that aid in managing the condition
        - Mindfulness, meditation, or stress-relief techniques used for symptom control
        - Support groups, community programs, or peer support for those with these conditions
        - Medical advice on managing side effects of medications or treatments
        - Any strategies aimed at improving mental health or reducing the impact of symptoms

        Respond with 'Yes' if the content explicitly mentions or strongly implies management strategies or advice related to the neurological diseases listed above. Respond with 'No' if it does not, or if the diseases are mentioned without specific information about management."""},

        {"role": "user", "content": f"""Analyze the following text and determine if it contains any mention of management strategies for neurological diseases as described above.

        Text: "{question}"

        Provide your answer in 'Yes' or 'No' one word only:"""}
    ]

    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=5,
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
            return answer
        else:
            print(f"Empty response for question: {question}")
            return "None"

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Problematic' or handle the error in another way
        return "Problematic"
    
# summarize content
def summarize(question):
    # Construct the messages for the chat completion
    messages = [
        {"role": "system", "content": """You are an AI assistant skilled in analyzing text to identify the main topic. Your task is to review the provided content and:

        Identify the primary topic or theme discussed.

        To determine the key topic, consider the following:
        - Focus on the central idea or most frequently mentioned subject.
        - Identify key issues, challenges, or solutions mentioned.
        - Determine what is essential for understanding the overall message.

        Your response should be concise and directly state the main topic"""},

        {"role": "user", "content": f"""Review the following content and:
        Identify the key topic or theme in a concise manner.

        Text: "{question}"
        
        Provide your answer as concisely as possible."""}
    ]

    try:
        response = client.chat.completions.create(
            model="benchChat",  # Use the appropriate model name
            messages=messages,  # Pass the messages instead of prompt
            max_tokens=50,  # Increase the max_tokens to allow a longer response if needed
            temperature=0  # Lower temperature for deterministic output
        )

        # Check if response and content exist before accessing
        if response and response.choices[0].message and response.choices[0].message.content:
            answer = response.choices[0].message.content.strip()  # Extract the answer from the message content
            return answer
        else:
            print(f"Empty response for question: {question}")
            return "None"

    except openai.BadRequestError as e:
        # Print the error message and the problematic question
        print(f"Error: {e}")
        print(f"Problematic question: {question}")
        # Return 'Problematic' or handle the error in another way
        return "Problematic"



#Loading data based on which LLM is going to answer:    
# questions = df['Content']

## *****************************************
#print("***Prompting Starts***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['diseases'] = df['Content'].apply(related_diseases)
#print("***Prompting Ends***")

#print("***Prompting Starts for medical_advice***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['medical_advice'] = df['Content'].apply(medical_advice)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for topic_identification***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['topic'] = df['Content'].apply(which_topic)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for related_to_workplace***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['workplace_related'] = df['Content'].apply(is_related_to_workplace)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for medical_medicine_related***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['medical_medicine_related'] = df['Content'].apply(medical_medicine_related)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for discrimination***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['discrimination'] = df['Content'].apply(discrimination)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for medicine_related_content***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['medicine_related'] = df['Content'].apply(medicine_related_content)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for relational_challenges***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['relational_challenges'] = df['Content'].apply(relational_challenges)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for social_emotional_challenges***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['social_emotional_challenges'] = df['Content'].apply(social_emotional_challenges)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

#print("***Prompting Starts for managing_diseases***")
## Apply the extract_hashtags function to each post in the DataFrame
#df['managing_diseases'] = df['Content'].apply(managing_diseases)
#print("***Prompting Ends***")
#df.to_csv(path, index=False)

print("***Prompting Starts for Summarize***")
# Apply the extract_hashtags function to each post in the DataFrame
df['summarize'] = df['Content'].apply(summarize)
print("***Prompting Ends***")
df.to_csv(path, index=False)
