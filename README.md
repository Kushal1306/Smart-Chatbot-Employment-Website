# Smart-Chatbot-Employment-Website
 An intelligent chatbot built on top of GPT-3.5 to fulfil users’ needs. It extracts the intent and entities of user queries and
 based on them, recommends jobs and events, and retrieves information from the knowledge base(MongoDB) using the nearest match
 approach. The model (BERT) was finetuned to extract intent and spacy was used to extract entities of a query.

 Example Snapshot
 ![323459775-9dd33ccb-b42d-4bbc-863e-dc3ce85dc33b](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/b57d30d9-3fa3-46ea-9b58-0f79b46bce93)

 
The whole methodology is categorised into the below steps: i.e
<br>
•	Data collection: collecting different types of queries (data) from various sources and labelling them with the probable intents
•	Annotating the collected queries with entities for entity recognition.
•	Training the Bert model on labelled queries for intent classification.
•	Training the spacy model for custom-named entity recognition.
•	Having a knowledge base that has a repository of different types of jobs.
•	Having a Large Language Model for Skill Development Suggestions.
•	Integrating all of the above with a user interface where users can enter queries and get recommendations

Data Collection:
Data was collected from various sources on the web, and textual expansion was done on those queries by changing the location and job type, resulting in an increase in the size of the data to 1339 queries. The figure in [1] demonstrates the same. All 1339 queries were labelled based on their nature and probable intent.

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/50b9ad5d-9c26-4dd5-a11a-c5d95adf1809)

Fig 1. Textual Expansion of Query
<br>
All queries were labelled with six different intents: job search, internship search, networking opportunities, skill development, career advice, and information retrieval. The picture in Figure 2 shows the distribution of queries across various intents.


 ![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/7d835421-4e60-4a33-a655-ff52f950421b)

Fig 2.  Bar Plot showing distribution of Queries over 6 Intents

<br>
The pre-trained BERT( Bidirectional Encoder Represenation Transformer) was fine-tuned on the above queries with the labelled intents for intent classification. Queries related to job search, internship search, and networking opportunities were annotated with probable entities as shown in figure 3.

 ![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/7ed4cfbf-bb45-4842-86ed-effbfadfd5fa)

Fig 3. Annotation of Query for Custom NER

All the annotated data was used to train the spacy model for custom-named entity recognition; the best model was used during the whole implementation. MongoDB was used as a knowledge base, which has data on the collection of jobs. Figure 4 shows the architecture of the whole methodology.
 
 
 ![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/48401907-34b5-4a07-91ed-113d2c95e384)

. Fig 4. Architecture of  Proposed Method

Whenever a user enters a query, the query is passed on to the Bert model for intent classification.
1.	If the intent is job search, internship search, or networking opportunities, the query will be passed to the spacy model for entity recognition, where entities get recognised like job type and location. The records from the knowledge base that match either partially or fully with the main entity “JobType” get retrieved.
Each record is then ranked and scored using the nearest match approach based on the number of entities matched with the data in the record. The record (Job) with the highest score then gets recommended  to the user in an understandable way.

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/d0525d4e-9aba-4d1f-b12c-be994c2120e9)

Fig 5. Scoring The Retrived Jobs Based on Users Query

2.	If the intent is Career Advice, skill development and information retrieval. Then The query is passed on to the large language model ( OpenAI’s GPT 3.5), whose response is recommended to the user.

IV. Results and Discussions
A smart chatbot to assist users of employment websites in job search, skill development, career advice, and networking opportunities was obtained, which was built using a fine-tuned BERT model for intent recognition and a spacy model for custom-named entity recognition. The chatbot was integrated with OpenAI’s GPT 3.5 for career advice and a knowledge base for recommending jobs. Gradio was used to build the interface of the chatbot.
Below are the figures for various features of the chatbot.
Figure 6 shows the user interface of the smart chatbot.

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/254f1467-3d9b-45c8-8449-db97e0dfc6fa)

Fig 6. UI of Chatbot (Built using Gradio)

Figure 7 shows the chatbot recommending the job that matches the user's needs. The intent of which is job search.

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/9dd33ccb-b42d-4bbc-863e-dc3ce85dc33b)

Fig 7. Chatbot Recommending the job which matches users query

Figure 8 shows the chatbot recommending an internship that matches the user's needs, where the intent of the user is an internship search.

 ![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/cab049d3-a2c1-4699-9792-a31ab34f0edf)

Fig 8. Chatbot Recommending Intership 
Figure 9 shows the chatbot giving career advice according to the user's needs, where the intent of the user is career advice.

 ![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/2874f0ac-7aeb-43d3-a8af-e24119cc8ccd)

Fig 9. Chatbot Giving Career Advices


Figure 10 shows the chatbot giving skill development suggestions according to the user's needs, where the intent of the user is skill development.

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/5ae2f465-5419-4783-8ee8-4e2712d639b9)

Fig 10. Chatbot Giving Skill Development Advices
Figure 11 shows the chatbot giving information according to the user's needs, where the intent of the user is information retrieval.

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/239648f7-8dbd-4c1b-9f3d-cf6b3f29e213)

Fig 11. Chatbot Answering Information Retrieval Query
There were five training iterations of the  bert model, each round had 42 batches of samples. As the training progressed, there was a similar pattern: every time the model becomes more accurate on the training data and thus its loss decreases step by step. In the beginning, the model’s loss was 1.0067 with 65.12% accuracy but they significantly changed in subsequent rounds to give accuracy of 99.93% and loss of 0.0204 as final results. On validation data, the models performance fluctuated with an accuracy range between 72.86% and 83.57%, while its loss varied from 0.4712 to 0.6391. As the size of the data was less. The model fails to generalize in few cases. Going forward the model with be able to generalize well, with more data collection and finetuning. The figure 12 shows training accuracy and loss over the course of iterations

![image](https://github.com/Kushal1306/Smart-Chatbot-Employment-Website/assets/95643826/f96b5ee1-4b77-4169-a1ee-40bced55e9cb)

Fig 12. Loss and Accuracy Plot of Training and Validation Phase

