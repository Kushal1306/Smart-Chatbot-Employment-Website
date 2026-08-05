import git
import os
from pathlib import Path

import deeplake
import requests
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from huggingface_hub import HfApi

load_dotenv(Path(__file__).resolve().parent / ".env")

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {"device": "cpu"}
allowed_extensions = ['.py', '.ipynb', '.md']
os.environ['ACTIVELOOP_TOKEN'] = os.getenv('ACTIVELOOP_TOKEN', '')
api = HfApi()
model_name = "facebook/bart-base"  # Replace with your desired Hugging Face model
model_info = api.model_info(model_name)
inference_url = model_info.pipeline_tag


class Embedder:
    def __init__(self,git_link) -> None:
        self.git_link=git_link
        last_name=self.git_link.split('/')[-1]
        self.clone_path=last_name.split('.')[0]
        self.deeplake_path = f"hub://kalakushaljain/{self.clone_path}"
        #self.model=
        self.hf=HuggingFaceEmbeddings(model_name=model_name)
        self.memory_buffer=ConversationBufferMemory(
            memory_key="chat_history",
            max_size=2
            )
    
    def add_to_queue(self,value):
        self.memory_buffer.add(value)
    
    def clone_repository(self):
        if not os.path.exist(self.clone_path):
            git.Repo.clone_from(self.git_link,self.clone_path)

    def extract_files(self):
        root_directory=self.clone_path
        self.docs=[]
        for dirpath, dirnames, filenames in os.walk(root_directory):
            for file in filenames:
                try:
                    loader=TextLoader(os.path.join(dirpath,file),encoding='utf-8')
                    self.docs.extend(loader.load_and_split)
                except Exception as e:
                    pass
    
    def chunk_files(self):
        text_splitter=CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
        self.texts=text_splitter.split_documents(self.docs)
        self.num_texts=len(self.texts)
    
    def embedd_using_deeplake(self):

        db=DeepLake(dataset_path=self.deeplake_path,embedding_function=self.hf)
        db.add_documents(self.texts)
        self.delete_directory(self.clone_path)

        return db
    
    def delete_directory(self,path):
        if os.path.exists(path):
            for root,dirs,files in os.walk(path,topdown=False):
                for file in files:
                    file_path=os.path.join(root,file)
                    os.remove(file_path)
                for dir in dirs:
                    dir_path=os.path.join(root,dir)
                    os.rmdir(dir_path)
            os.rmdir(path)
    
    def load_db(self):
        exists=deeplake.exist(self.deeplake_path)
        if exists:
            self.db=DeepLake(
                dataset_path=self.deeplake_path,
                read_only=True,
                embedding_function=self.hf,
            )
        else:
            self.extract_files()
            self.chunk_files()
            self.db=self.embedd_using_deeplake()


        self.retriever=self.db.as_retriever()
        self.retriever.search_kwargs['distance_metric']='cos'
        self.retriever.search_kwargs['fetch_k']=100
        self.retriever.search_kwargs['maximal_marginal_relevance']=True
        self.retriever.search_kwargs['k']=3
    
    def retrieve_results(self, query):
        chat_history = self.memory_buffer.get_buffer()
        headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_TOKEN', '')}"}
        data = {"inputs": query, "chat_history": chat_history}  # Adjust as needed

        response = requests.post(inference_url, headers=headers, json=data)
    
        if response.status_code == 200:
            result = response.json()
            answer = result.get("generated_text", "")
             # Initialize the conversational chain with the generated text
            qa = ConversationalRetrievalChain.from_text(
            answer, chain_type="stuff", retriever=self.retriever
                )
            # Process the query within the initialized chain
            result = qa({"question": query})
        
             # Add the query-answer pair to the queue
            self.add_to_queue((query, result["answer"]))
        
            return result['answer']
        else:
            # Handle API request failure
            return "Failed to retrieve answer from the inference API"

    