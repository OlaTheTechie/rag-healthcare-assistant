# import streamlit as st
# from streamlit_chat import message
# from src.model import setup_chatbot_chain

# chatbot = setup_chatbot_chain()

# st.title("Healthcare Support Agent.")


# def conversation_chat(query): 
#     result = chatbot({"question": query, "chat-history": st.session_state["history"]})
#     st.session_state["history"].append((query, result["answer"]))

#     return result["answer"]


# def initialize_session_state():
#     if "history" not in st.session_state: 
#         st.session_state["history"] = []

#     if "generated" not in st.session_state: 
#         st.session_state["generated"] = ["Hello, ask me anything"]

#     if "past" not in st.session_state: 
#         st.session_state["past"] = ["Hey there!"]

# def display_chat_history(): 
#     reply_container = st.container()
#     container = st.container()

#     with container: 
#         with st.form(key="my-form", clear_on_submit=True): 
#             user_input = st.text_input("Question: ", placeholder="Ask me about your health")
#             submit_btn = st.form_submit_button(label="Send")

#             if submit_btn and user_input: 
#                 output = conversation_chat(query=user_input)
#                 st.session_state["past"].append(user_input)
#                 st.session_state["generated"].append(output)
#     if st.session_state["generated"]:
#         with reply_container: 
#             for i in range(len(st.session_state["generated"])): 
#                 message(
#                 st.session_state["past"][i], 
#                 is_user=True, 
#                 key=f"user_{i}",  # Unique key for user messages
#                 avatar_style="thumbs"
#                 )
                 
#                 message(
#                 st.session_state["generated"][i], 
#                 is_user=False, 
#                 key=f"bot_{i}",  # Unique key for bot responses
#                 avatar_style="bottts"
#                 )


# # initialise session
# initialize_session_state()

# # display chats
# display_chat_history()


import streamlit as st
from streamlit_chat import message
from src.model import setup_chatbot_chain

# Initialize the chatbot chain (this should only be done once)
chatbot = setup_chatbot_chain()

st.title("Healthcare Support Agent.")

# Ensure session state is properly initialized
def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state["history"] = []

    if "generated" not in st.session_state:
        st.session_state["generated"] = ["Hello, ask me anything"]

    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey there!"]

# Function to interact with the chatbot
def conversation_chat(query):
    # Use the initialized chatbot chain to get the response
    result = chatbot({"question": query})

    # Append the result to session state
    st.session_state["history"].append((query, result["answer"]))
    
    return result["answer"]

# Function to display the chat history
def display_chat_history(): 
    reply_container = st.container()
    container = st.container()

    with container: 
        with st.form(key="my-form", clear_on_submit=True): 
            user_input = st.text_input("Question: ", placeholder="Ask me about your health")
            submit_btn = st.form_submit_button(label="Send")

            if submit_btn and user_input: 
                output = conversation_chat(query=user_input)
                st.session_state["past"].append(user_input)
                st.session_state["generated"].append(output)
    
    if st.session_state["generated"]:
        with reply_container: 
            for i in range(len(st.session_state["generated"])): 
                message(
                    st.session_state["past"][i], 
                    is_user=True, 
                    key=f"user_{i}",  # Unique key for user messages
                    avatar_style="thumbs"
                )
                 
                message(
                    st.session_state["generated"][i], 
                    is_user=False, 
                    key=f"bot_{i}",  # Unique key for bot responses
                    avatar_style="bottts"
                )

# Initialize session state
initialize_session_state()

# Display the chat interface
display_chat_history()
