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

path = 'Data/merged_comments.csv'
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

#Loading data based on which LLM is going to answer:    
questions = df['Content']

print("***Prompting Starts***")
results = {question: medicine_related_content(question) for question in questions}
print("***Prompting Ends***")


l = []
text = []
for question, answer in results.items():
    l.append(answer)
    text.append(question)
    # print(f"Question: {question}\nAnswer: {answer}\n")

print(len(l))
print(len(text))

merged_list = list(zip(text, l))

df = pd.DataFrame(merged_list, columns=['Content', 'medicine_related'])
print(df)

merged_df = pd.merge(df_org, df, on='Content', how='right')
print(merged_df)

merged_df.to_csv(path, index=False)
