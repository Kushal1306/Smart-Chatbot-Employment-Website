# -*- coding: utf-8 -*-
"""Intent_Recognition_and_Entity_Recognition_main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QjnJr3C_BVAFnAhMNpENTa6wMrQXpMlF
"""

!pip install -U "tensorflow-text==2.13.*"

!pip install "tf-models-official==2.13.*"

import os
#import shutil
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import seaborn as sns
from pylab import rcParams

import matplotlib.pyplot as plt
tf.get_logger().setLevel('ERROR')

sns.set(style='whitegrid', palette='muted', font_scale=1.2)
HAPPY_COLORS_PALETTE = ["#01BEFE", "#FFDD00", "#FF7D00", "#FF006D", "#ADFF02", "#8F00FF"]
sns.set_palette(sns.color_palette(HAPPY_COLORS_PALETTE))
rcParams['figure.figsize'] = 12, 8
import warnings
warnings.filterwarnings("ignore")

traindf = pd.read_csv("train.csv")
validdf = pd.read_csv("valid.csv")
testdf = pd.read_csv("test.csv")

traindf.head()

trainfeatures=traindf.copy()
trainlabels=trainfeatures.pop("intent")

trainfeatures=trainfeatures.values

traindf.shape

chart = sns.countplot(trainlabels, palette=HAPPY_COLORS_PALETTE)
plt.title("Number of texts per intent")
chart.set_xticklabels(chart.get_xticklabels(), rotation=30, horizontalalignment='right');

from sklearn.preprocessing import LabelBinarizer

binarizer=LabelBinarizer()
trainlabels=binarizer.fit_transform(trainlabels.values)

trainlabels.shape

testfeatures=testdf.copy()
testlabels=testfeatures.pop("intent")
validfeatures=validdf.copy()
validlabels=validfeatures.pop("intent")

testfeatures=testfeatures.values
validfeatures=validfeatures.values

testlabels=binarizer.transform(testlabels.values)
validlabels=binarizer.transform(validlabels.values)

bert_model_name = 'small_bert/bert_en_uncased_L-8_H-512_A-8'
map_name_to_handle = {
    'bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/3',
    'bert_en_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_cased_L-12_H-768_A-12/3',
    'bert_multi_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_multi_cased_L-12_H-768_A-12/3',
    'small_bert/bert_en_uncased_L-2_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-2_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-2_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-2_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-4_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-4_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-4_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-4_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-6_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-6_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-6_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-6_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-6_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-8_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-8_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-8_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-8_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-8_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-10_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-10_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-10_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-10_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-10_H-768_A-12/1',
    'small_bert/bert_en_uncased_L-12_H-128_A-2':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-128_A-2/1',
    'small_bert/bert_en_uncased_L-12_H-256_A-4':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-256_A-4/1',
    'small_bert/bert_en_uncased_L-12_H-512_A-8':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-512_A-8/1',
    'small_bert/bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-12_H-768_A-12/1',
    'albert_en_base':
        'https://tfhub.dev/tensorflow/albert_en_base/2',
    'electra_small':
        'https://tfhub.dev/google/electra_small/2',
    'electra_base':
        'https://tfhub.dev/google/electra_base/2',
    'experts_pubmed':
        'https://tfhub.dev/google/experts/bert/pubmed/2',
    'experts_wiki_books':
        'https://tfhub.dev/google/experts/bert/wiki_books/2',
    'talking-heads_base':
        'https://tfhub.dev/tensorflow/talkheads_ggelu_bert_en_base/1',
}

map_model_to_preprocess = {
    'bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'bert_en_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_cased_preprocess/2',
    'small_bert/bert_en_uncased_L-2_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-2_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-2_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-2_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-4_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-4_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-4_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-4_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-6_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-6_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-6_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-6_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-8_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-8_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-8_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-8_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-10_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-10_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-10_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-10_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-12_H-128_A-2':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-12_H-256_A-4':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-12_H-512_A-8':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'small_bert/bert_en_uncased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'bert_multi_cased_L-12_H-768_A-12':
        'https://tfhub.dev/tensorflow/bert_multi_cased_preprocess/2',
    'albert_en_base':
        'https://tfhub.dev/tensorflow/albert_en_preprocess/2',
    'electra_small':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'electra_base':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'experts_pubmed':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'experts_wiki_books':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
    'talking-heads_base':
        'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2',
}

tfhub_handle_encoder = map_name_to_handle[bert_model_name]
tfhub_handle_preprocess = map_model_to_preprocess[bert_model_name]

print(f'BERT model selected           : {tfhub_handle_encoder}')
print(f'Preprocess model auto-selected: {tfhub_handle_preprocess}')

bert_preprocess_model = hub.KerasLayer(tfhub_handle_preprocess)

trainfeatures[0]

text_test = trainfeatures[0]
text_preprocessed = bert_preprocess_model(text_test)

print(f'Keys       : {list(text_preprocessed.keys())}')
print(f'Shape      : {text_preprocessed["input_word_ids"].shape}')
print(f'Word Ids   : {text_preprocessed["input_word_ids"][0, :12]}')
print(f'Input Mask : {text_preprocessed["input_mask"][0, :12]}')
print(f'Type Ids   : {text_preprocessed["input_type_ids"][0, :12]}')

bert_model = hub.KerasLayer(tfhub_handle_encoder)

bert_results = bert_model(text_preprocessed)

print(f'Loaded BERT: {tfhub_handle_encoder}')
print(f'Pooled Outputs Shape:{bert_results["pooled_output"].shape}')
print(f'Pooled Outputs Values:{bert_results["pooled_output"][0, :12]}')
print(f'Sequence Outputs Shape:{bert_results["sequence_output"].shape}')
print(f'Sequence Outputs Values:{bert_results["sequence_output"][0, :12]}')

def build_classifier_model():
  text_input = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
  preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name='preprocessing')
  encoder_inputs = preprocessing_layer(text_input)
  encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name='BERT_encoder')
  outputs = encoder(encoder_inputs)
  net = outputs['pooled_output']
  net = tf.keras.layers.Dropout(0.1)(net)
  net = tf.keras.layers.Dense(6, activation=None, name='classifier')(net)
  return tf.keras.Model(text_input, net)

classifier_model = build_classifier_model()
bert_raw_result = classifier_model(tf.constant(trainfeatures[0]))
print(tf.keras.activations.softmax(bert_raw_result))

classifier_model.summary()

loss = tf.keras.losses.CategoricalCrossentropy(from_logits=True)
metrics = tf.metrics.CategoricalAccuracy()

epochs=5
optimizer=tf.keras.optimizers.Adam(1e-5)
classifier_model.compile(optimizer=optimizer,
                         loss=loss,
                         metrics=metrics)



print(f'Training model with {tfhub_handle_encoder}')
history = classifier_model.fit(x=trainfeatures,y=trainlabels,
                               validation_data=(validfeatures,validlabels),
                               batch_size=32,
                               epochs=epochs)

loss, accuracy = classifier_model.evaluate(testfeatures,testlabels)

print(f'Loss: {loss}')
print(f'Accuracy: {accuracy}')

history_dict = history.history
print(history_dict.keys())

acc = history_dict['categorical_accuracy']
val_acc = history_dict['val_categorical_accuracy']
loss = history_dict['loss']
val_loss = history_dict['val_loss']

epochs = range(1, len(acc) + 1)
fig = plt.figure(figsize=(10, 8))
fig.tight_layout()

plt.subplot(2, 1, 1)
# "bo" is for "blue dot"
plt.plot(epochs, loss, 'r', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.grid(True)
# plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(epochs, acc, 'r', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.grid(True)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

def print_my_examples(inputs, results):
  result_for_printing = \
    [f'input: {inputs[i]:<30} : estimated intent: {results[i]}'
                         for i in range(len(inputs))]
  print(*result_for_printing, sep='\n')
  print()


examples = [
    'search me software jobs in hyderabad',  # this is the same sentence tried earlier
    'give me career advice to be a engineer',
    'give me information for how to apply for jobs',
    'suggest me full stack jobs in amritsar',
    'give me plumbing jobs in vizag'
]

results = tf.nn.softmax(classifier_model(tf.constant(examples)))

binarizer.classes_

intents=binarizer.inverse_transform(results.numpy())

print_my_examples(examples, intents)

def get_intent(text):
    result = tf.nn.softmax(classifier_model(tf.constant([text])))
    intent = binarizer.inverse_transform(result.numpy())[0]
    return intent

def process_input():
    while True:
        text = input("Enter your query (type 'exit' to quit): ")
        if text.lower() == 'exit':
            print("Exiting...")
            break
        intent = get_intent(text)
        print(f"Input: {text} - Estimated Intent: {intent}")
        print()

# Example usage
process_input()

# Save the model
classifier_model.save("intent_classifier_model")

# Save the binarizer
import joblib
joblib.dump(binarizer, "intent_binarizer.joblib")

from tensorflow.keras.models import load_model

def load_model_and_binarizer():
    # Load the model
    classifier_model = load_model("intent_classifier_model")

    # Load the binarizer
    binarizer = joblib.load("intent_binarizer.joblib")

    return classifier_model, binarizer

def get_intent(text, classifier_model, binarizer):
    result = tf.nn.softmax(classifier_model(tf.constant([text])))
    intent = binarizer.inverse_transform(result.numpy())[0]
    return intent

def process_input(classifier_model, binarizer):
    while True:
        text = input("Enter your query (type 'exit' to quit): ")
        if text.lower() == 'exit':
            print("Exiting...")
            break
        intent = get_intent(text, classifier_model, binarizer)
       # print(f"Input: {text} - Estimated Intent: {intent}")
        print(intent)

# Load the model and binarizer
classifier_model, binarizer = load_model_and_binarizer()

# Process input
process_input(classifier_model, binarizer)

# from google.colab import drive
# drive.mount('/content/drive')
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Define the path to save the model and binarizer in Google Drive
model_path = '/content/drive/My Drive/intent_classifier_model'
binarizer_path = '/content/drive/My Drive/intent_binarizer.joblib'

# Save the model
classifier_model.save(model_path)

# Save the binarizer
joblib.dump(binarizer, binarizer_path)

from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')
model_path = '/content/drive/My Drive/models/intent_classifier_model'
binarizer_path = '/content/drive/My Drive/models/intent_binarizer.joblib'
def load_model_and_binarizer():
    # Load the model
    classifier_model = load_model(model_path)

    # Load the binarizer
    binarizer = joblib.load(binarizer_path)

    return classifier_model, binarizer

def get_intent(text, classifier_model, binarizer):
    result = tf.nn.softmax(classifier_model(tf.constant([text])))
    intent = binarizer.inverse_transform(result.numpy())[0]
    return intent

def process_input(classifier_model, binarizer):
    while True:
        text = input("Enter your query (type 'exit' to quit): ")
        if text.lower() == 'exit':
            print("Exiting...")
            break
        intent = get_intent(text, classifier_model, binarizer)
       # print(f"Input: {text} - Estimated Intent: {intent}")
        print(intent)

# Load the model and binarizer
classifier_model, binarizer = load_model_and_binarizer()

# Process input
process_input(classifier_model, binarizer)

print(classifier_model)

"""# Named Entity Recognition
Recognizing entity after intent recogniton
"""

!pip install spacy

!python -m spacy download en_core_web_sm

import os
import pymongo
from pymongo import MongoClient
import openai
import streamlit as st

st.title("Punjab Govt's Employment Chatbot")

# Set your OpenAI API key
openai.api_key = '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'

# MongoDB connection setup
mongo_client = MongoClient("mongodb+srv://kushal:kushal789@cluster0.prccmls.mongodb.net/?retryWrites=true&w=majority")  # Update the MongoDB connection string
db = mongo_client["sih2023"]  # Replace with your MongoDB database name
collection = db["jobslitings"]  # Replace with your MongoDB collection name

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
    prompt = f"User Query: \"{user_input}\"\n strictly Recognize user query intent in two words. stricly just give intent in two words. categorize  the intent as anyone of i) job search, ii) skill development, iii)counseling, or iv) information retrieval.\""

    response = openai.Completion.create(
        engine="text-davinci-002",  # Use a text-based engine for intent recognition
        prompt=prompt,
        max_tokens=32,  # Adjust the response length as needed
    )

    # Extract the recognized intent from the response
    recognized_intent = response.choices[0].text.strip()
    print(recognized_intent)

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




user_input=st.text_input("Enter your query:")
print(user_input)

if st.button("Ask"):
    try:
         intent_response = classify_intent(user_input)
         print(intent_response)
         for line in intent_response.split('\n'):
             st.write(line)
    except Exception as e:

        st.write("Please Re-enter the query.")


    #st.write("Chatbot:",intent_response)

