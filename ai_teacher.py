import streamlit as st
import os
import openai
import base64
from PIL import Image as PILImage

GLHF_API_KEY = os.getenv("GLHF_API_KEY")

messages=[
    {"role": "system", "content": "Please act as an experienced secondary school teacher with expertise in the subject matter of the question. When I present questions: \n1. First break down the key concepts and principles involved \n2. Provide relatable real-world examples to illustrate each concept \n3. Guide me through the problem-solving approach using the Socratic method \n4. Include practice problems similar to but different from my original question \n5. Only provide the actual answer when I explicitly request it with 'Please show the solution' Please adjust the complexity of your explanations for a secondary school student (ages 14-18) and use clear, engaging language. Feel free to use diagrams or visual explanations when helpful."},
    ]

if "model_name" not in st.session_state:
    st.session_state["model_name"] = "hf:meta-llama/Llama-3.3-70B-Instruct"

client = openai.OpenAI(
    api_key=os.environ.get("GLHF_API_KEY"),
    base_url="https://glhf.chat/api/openai/v1",
    )

def create_chat():
    st.session_state["chat_session"] = [
    {"role": "system", "content": "Please act as an experienced secondary school teacher with expertise in the subject matter of the question. When I present questions: \n1. First break down the key concepts and principles involved \n2. Provide relatable real-world examples to illustrate each concept \n3. Guide me through the problem-solving approach using the Socratic method \n4. Include practice problems similar to but different from my original question \n5. Only provide the actual answer when I explicitly request it with 'Please show the solution' Please adjust the complexity of your explanations for a secondary school student (ages 14-18) and use clear, engaging language. Feel free to use diagrams or visual explanations when helpful."},
    ]


if "chat_session" not in st.session_state:
    create_chat()

def on_new_chat():
    create_chat()


st.sidebar.button("New Chat", on_click=on_new_chat)

st.markdown("#### Hello I am an AI Powered Teacher what shall we learn about today?")

question = st.chat_input("Ask me anything ...")
if question:
    st.markdown(f"*The student has asked me: {question}*")
    with st.spinner("Please wait a second or two while a I think about that ..."):
        st.session_state["chat_session"].append({"role": "user", "content": question})
        print (st.session_state["chat_session"])
        completion = client.chat.completions.create(
            model=st.session_state["model_name"],
            messages=st.session_state["chat_session"])
        response = (completion.choices[0].message.content)
        st.session_state["chat_session"].append({"role": "assistant", "content": response})
        st.markdown(response)