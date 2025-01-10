import streamlit as st
from streamlit_chat import message
from process import generate_response 

st.title("Healthcare Agentic Assistant")

def initialize_session_state():
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["Hello! How can I assist you today?"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey there!"]

initialize_session_state()

# Function to display chat history and interact with the assistant
def chat_interface():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Your Question:", placeholder="Please ask a question")
            submit_btn = st.form_submit_button(label="Send")

            if submit_btn and user_input:
                response = generate_response(user_input)
                # response = 'testing'
                # Append user and bot messages to session state
                st.session_state["past"].append(user_input)
                st.session_state["generated"].append(response)

    if st.session_state["generated"]:
        with reply_container:
            for i in range(len(st.session_state["generated"])):
                # Display user message
                message(
                    st.session_state["past"][i],
                    is_user=True,
                    key=f"user_{i}",
                    avatar_style="thumbs",
                )
                # Display bot response
                message(
                    st.session_state["generated"][i],
                    is_user=False,
                    key=f"bot_{i}",
                    avatar_style="bottts",
                )

chat_interface()
