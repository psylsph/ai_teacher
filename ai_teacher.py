import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os

def create_chat():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBud2LfN_RDdqpWGrlfwnR7Ya86Jo32Iag")
    genai.configure(api_key=GOOGLE_API_KEY)
    generation_config = {
        "temperature": 0.3,
        "top_p": 0.95,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    system_instructions = "Please act as an experienced secondary school teacher with expertise in the subject matter of the question. When I present questions: \n1. First break down the key concepts and principles involved \n2. Provide relatable real-world examples to illustrate each concept \n3. Guide me through the problem-solving approach using the Socratic method \n4. Include practice problems similar to but different from my original question \n5. Only provide the actual answer when I explicitly request it with 'Please show the solution' Please adjust the complexity of your explanations for a secondary school student (ages 14-18) and use clear, engaging language. Feel free to use diagrams or visual explanations when helpful."
    safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_LOW_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_LOW_AND_ABOVE"},
        ]
    model_object = genai.GenerativeModel(
    model_name=st.session_state["model_name"],
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=system_instructions,
    )

    st.session_state["session_google"] = model_object.start_chat(history=[])    

st.set_page_config(layout="wide")
if st.sidebar.button("New Chat"):
    print("Creating chat")
    create_chat()

st.sidebar.header("Configuration")
st.session_state["model_name"] = st.sidebar.selectbox("Select AI Agent:", options=["gemini-1.5-flash-8b-001", "gemini-1.5-flash-002", "gemini-2.0-flash-exp"], index=1)
st.markdown("#### Hello I am an AI Powered Teacher what shall we learn about today?")
st.session_state["question"] = st.sidebar.text_area("Enter your question here:")


if st.sidebar.button("Ask the Teacher"):
    with st.spinner("Mmm thats a good question wait a second or two while a I think about that ..."):
        response = st.session_state["session_google"].send_message(st.session_state["question"])
        st.write(response.text)
else:
    if not "session_google" in st.session_state:
        print("Creating chat")
        create_chat()
