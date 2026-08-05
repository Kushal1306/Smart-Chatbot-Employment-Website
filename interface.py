import streamlit as st
import os
import assignment


input_repository=st.text_input(" Enter Github link of the repository")

if input_repository:
    st.write("Entered Repository:",input_repository)
    st.write("Wait until your repository is being ")
     #command to load github repository
    
    #commands to parsing and embedding into vector store
    st.write("Shoot your questions")

    if "messages" not in st.session_state:
        st.session_state.messages=[]
   
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt=st.chat_input("Enter your query")
    if prompt:
        
        st.session_state.messages.append({"role":"user","content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        #command to answer from the LLM and retreival
        #reponse=

# Define your Streamlit content
