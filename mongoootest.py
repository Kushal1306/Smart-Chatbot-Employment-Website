# !pip install openai pymongo streamlit

import os
import pymongo
from pymongo import MongoClient
import openai
import streamlit as st

st.title("Punjab Govt's Employment Chatbot")

# MongoDB connection setup
mongo_client = MongoClient("mongodb://localhost:27017/")  # Update the MongoDB connection string
db = mongo_client["sih2023"]  # Replace with your MongoDB database name
collection = db["jobslitings1"]  # Replace with your MongoDB collection name

# Connect to your MongoDB server
# client = pymongo.MongoClient("mongodb+srv://kushal:agXPt0UNyEmNaHU@cluster0.prccmls.mongodb.net/?retryWrites=true&w=majority")
# db = client.sih2023
# collection = db.joblistings

def chatbot(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the GPT-3.5 Turbo model
        messages=[
            {"role": "system", "content": "You are a chatbot of Punjab governments employement website.Just full fill users query in 4-5 lines. dont act like an chatbot."},
            {"role": "user", "content": input_text},
        ],
    )
    return response.choices[0].message["content"]

def extract_intent_from_gpt3_response(user_input):
    # Use GPT-3.5 Turbo to recognize the intent
    prompt = f"User Query: \"{user_input}\"\n strictly Recognize user query intent in two words. stricly just give intent in two words. categorize  the intent as anyone of job search, skill development counseling, or information retrieval.\""

    response = openai.Completion.create(
        engine="text-davinci-002",  # Use a text-based engine for intent recognition
        prompt=prompt,
        max_tokens=32,  # Adjust the response length as needed
    )

    # Extract the recognized intent from the response
    recognized_intent = response.choices[0].text.strip()

    return recognized_intent

# Define your intent classification and response generation functions as needed

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
    # Check the recognized intent against the mapping
    recognized_intent_lower = recognized_intent.lower()

    if recognized_intent_lower in intent_mapping:
        # Determine the intent category
        intent_category = intent_mapping[recognized_intent_lower]

        # Implement logic based on the intent category
        if intent_category == "Job Search":
            # Handle job search queries
            response = respond_to_job_search_query(user_input)
        elif intent_category == "Skill Development":
            # Handle skill development inquiries
           # response = respond_to_skill_development_query(user_input)
             response=chatbot(user_input)
        elif intent_category == "Counseling":
            # Handle counseling requests
            #response = respond_to_counseling_query(user_input)
            response=chatbot(user_input)
        # Add more conditions for other intent categories
        elif intent_category=="Information Retrieval":

            response=chatbot(user_input)
    else:
        # Handle unrecognized intents or fallback responses
        #response = respond_to_unrecognized_intent(user_input)
        response=chatbot(user_input)

    return response

def extract_entities(user_input):
    prompt = f"User Query: \"{user_input}\"\nRecognize entities in the user query, stricly identify the role and location only, and present them separated by a comma.\""

    response = openai.Completion.create(
        engine="text-davinci-002",  # Use a text-based engine for intent recognition
        prompt=prompt,
        max_tokens=32,  # Adjust the response length as needed
    )

    # Extract the recognized intent from the response
    recognized_entities = response.choices[0].text.strip()

    return recognized_entities

def respond_to_job_search_query(user_input):
    # Your logic to respond to job search queries goes here
    # For this example, we return a predefined response
    sentence_entites=extract_entities(user_input)
    role, location = map(str.strip, sentence_entites.split(','))
    print(role)
    print(location)
    query={"role":role}
    jobs=collection.find(query)
    matching_jobs=list(jobs)

    #print(matching_jobs)

    # Scoring criteria
   # entity = job_role  # For title match
    job_scores = []
# Iterate through job listings and calculate scores
    for job in matching_jobs:
      #print(job)
      score = 0

      if job["role"].lower() ==role.lower():
        score += 1

      if job["location"].lower() == location.lower():
        score += 1

    # # Skills match
    # for skill in job["skills_required"]:
    #     if skill.lower() == entity.lower():
    #         score += 1
      job_scores.append({"job_title": job["role"],"location":job["location"], "description":job["description"],"salary":job["salary"],"Application_link":job["application_link"],"score": score})

# Sort job listings by score in descending order
    job_scores.sort(key=lambda x: x["score"], reverse=True)
    #print(job_scores)

    # Get the best recommendation
    if job_scores:
      best_recommendation = job_scores[0]
      print(best_recommendation)

      response =(
        f"Here is the best job listing that matches your criteria:\n"
        f"Job Title: {best_recommendation['job_title']}\n"
        f"Location: {best_recommendation['location']}\n"  # Use the provided location
        f"Salary: {best_recommendation['salary']}\n"
        f"Description: {best_recommendation['description']}\n"
        f"Link to Apply:{best_recommendation['Application_link']}\n"
        f"Score: {best_recommendation['score']}\n"
      )
       # Generate a user-friendly response for the best recommendation
    else:
      response = "No matching job listings found."

# Present the response to the user
    return response

def respond_to_skill_development_query(user_input):
    prompt = f"User Query: \"{user_input}\"\n Can you suggest resources for user query in unpto 4-5 lines maximum\""
    response=openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=128
    )

    recognized_skill=response.choices[0].text.strip()

    # Your logic to respond to skill development inquiries goes here
    # For this example, we return a predefined response
    return recognized_skill

def respond_to_counseling_query(user_input):
    # Your logic to respond to counseling requests goes here
    # For this example, we return a predefined response
    return "Here is information on counseling services."

def respond_to_unrecognized_intent(user_input):
    # Your logic to respond to unrecognized intents or provide a fallback response
    # For this example, we return a generic response
    return "I'm sorry, I couldn't understand your query."


# Your previous code here...

#def generate_response_from_mongodb(user_input):
    # Your logic to generate a response from MongoDB goes here
    # This is where you would query your MongoDB database
    # For this example, we return a predefined response
    # result = collection.find_one({"user_input": user_input})
    # if result:
    #     return result["response"]
    # else:
    #     return "No data found in the database."

# while True:
#     user_input = input("Please enter the query: ")
#     intent_response = classify_intent(user_input)

#     # if intent == "information retrieval":
#     #     response = retrieve_info_from_finetuned_model(intent)
#     # else:
#     #     response = generate_response_from_mongodb(user_input)

#     print("Chatbot:", intent_response)

user_input=st.text_input("Enter your query:")

if st.button("Ask"):
    try:
         intent_response = classify_intent(user_input)
         for line in intent_response.split('\n'):
             st.write(line)
    except Exception as e:

        st.write("Please Re-enter the query.")

   
    #st.write("Chatbot:",intent_response)

