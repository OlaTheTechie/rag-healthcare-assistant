from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
import faiss
import streamlit as st
from langchain_community.llms import CTransformers


data_path = "data/"
faiss_db_path = "vectorstore/faiss_db"

def create_vector_db(): 
    loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

    # database 
    db = FAISS.from_documents(text_chunks, embeddings)
    db.save_local(faiss_db_path)



if __name__ == "__main__": 
    create_vector_db()
    print("Database created sucessfully")
    print("Data saved in local database successfully")