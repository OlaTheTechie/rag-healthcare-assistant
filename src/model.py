# from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import CTransformers
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import FAISS
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import RetrievalQA, ConversationalRetrievalChain
# import faiss
# import streamlit as st

# from langchain import PromptTemplate



# faiss_db_path = "vectorstore/faiss_db"

# custom_prompt_template = """
#     Use the following piece of information to answer user's questions. 
#     If you don't know the answer, please just say that you don't, don't try to make things up

#     Context:{}
#     Question:{question}

#     Only return the helpful answer and nothing more.
# """

# def set_costum_template(): 
#     """
#     Prompt template for QA retriever
#     """

#     prompt = PromptTemplate(
#         template=custom_prompt_template, input_variables=["context", "question"]
#     )

#     return prompt


# def load_llm(): 
#     llm = CTransformers(
#         model="models/llama-2-7b-chat.ggmlv3.q4_0.bin", 
#         model_type="llama", 
#         config={"max_new_tokens":28, "temperature":0.01}
#         )
#     return llm



# def retrieval_qa_chain(llm, db, prompt): 
#     retrieval_qa = RetrievalQA.from_chain_type(
#         llm=llm,
#         retriever=db.as_retriever(search_kwargs={"k": 3}),
#         return_source_documents=True
#     )
#     return retrieval_qa


# def qa_bot(): 
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={"device": "cpu"})

#     db = FAISS.load_local(faiss_db_path, embeddings, allow_dangerous_deserialization=True)
#     llm=load_llm()
#     qa_prompt = set_costum_template()
#     qa = retrieval_qa_chain(llm, db, qa_prompt)

#     return qa


# def final_result(query): 
#     result = qa_bot()
#     response = result({"query": query})
#     return response



from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import faiss
import streamlit as st
from langchain.prompts import PromptTemplate

# Path to the FAISS database
faiss_db_path = "vectorstore/faiss_db"

# Custom prompt template for the chatbot
custom_prompt_template = """
    Use the following context to answer the user's question as accurately as possible.
    If you do not know the answer, say so. Do not fabricate information.

    Context: {context}
    Question: {question}

    Provide only a concise and helpful response.
"""

# Function to create the custom prompt template
def set_custom_template():
    prompt = PromptTemplate(
        template=custom_prompt_template, 
        input_variables=["context", "question"]
    )
    return prompt

# Function to load the LLM
def load_llm():
    llm = CTransformers(
        model="models/llama-2-7b-chat.ggmlv3.q4_0.bin",
        model_type="llama",
        config={"max_new_tokens": 200, "temperature": 0.01}
    )
    return llm

# Function to set up the Conversational Retrieval Chain
def setup_chatbot_chain():
    # Load embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # Load FAISS database
    db = FAISS.load_local(faiss_db_path, embeddings, allow_dangerous_deserialization=True)

    # Load the LLM
    llm = load_llm()

    # Create memory to track conversation history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Define the custom prompt
    custom_prompt = set_custom_template()

    # Create Conversational Retrieval Chain
    chatbot_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": custom_prompt}
    )
    return chatbot_chain

