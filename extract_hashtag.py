import pandas as pd
import re

#function
def extract_hashtags(text):
    if isinstance(text, str):
        hashtags = re.findall(r'#\w+', text)
        return hashtags if hashtags else "No hashtags found"  # Return message if no hashtags
    return "No hashtags found"  # Return message for non-string values

#data 
path = 'Data/all_posts.csv'
df = pd.read_csv(path)

# Apply the extract_hashtags function to each post in the DataFrame
df['hashtags'] = df['Content'].apply(extract_hashtags)

# Print the DataFrame with the new column
print(df[['Content', 'hashtags']])

df.to_csv(path, index=False)
