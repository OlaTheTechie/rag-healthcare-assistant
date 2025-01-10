from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
api_key = st.secrets[API_KEY"]

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", 
                                   model_kwargs={"device": "cpu"})

vector_store = FAISS.load_local("vector_store/faiss_db", embeddings, allow_dangerous_deserialization=True)
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=api_key)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        memory=memory
    )

def generate_response(prompt):
    return chain.run(prompt)
