import os
from pathlib import Path

import openai
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_intent_from_gpt3_response(user_input):
    # Use GPT-3.5 Turbo to recognize the intent
    prompt = f"User Query: \"{user_input}\"\n Categorize the intent of the query(strictly give only intent. no extra text.) as one of the following. job search,  skill development, counseling, or information retrieval."

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Use a text-based engine for intent recognition
        prompt=prompt,
        max_tokens=32,  # Adjust the response length as needed
    )

    # Extract the recognized intent from the response
    recognized_intent = response.choices[0].text.strip()

    return recognized_intent

def classify_intent(user_input):
    # Your intent classification logic goes here
    # You may use NLP models or libraries to classify intents
    recognized_intent = extract_intent_from_gpt3_response(user_input)

    # Map recognized intent to predefined categories
    intent_mapping = {
        "job search": "Job Search",
        "skill development": "Skill Development",
        "counseling": "Counseling",
        "information retrieval":"Information Retrieval"
        # Add more mappings as needed
    }
    print(recognized_intent)

user_input=input("enter the text:")
intent_response = classify_intent(user_input)
#print(intent_response)