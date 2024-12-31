import streamlit as st
import google.generativeai as genai
import os
import base64
from PIL import Image as PILImage

if "model_name" not in st.session_state:
    st.session_state["model_name"] = "gemini-1.5-flash-002"

def create_chat():
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
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
    print("Chat session started")

if "session_google" not in st.session_state:
    create_chat()

def on_new_chat():
    create_chat()

st.set_page_config(layout="wide")

st.sidebar.button("New Chat", on_click=on_new_chat)
  

st.sidebar.header("Configuration")
st.session_state["model_name"] = st.sidebar.selectbox("Select AI Agent:", options=["gemini-1.5-flash-8b-001", "gemini-1.5-flash-002", "gemini-2.0-flash-exp"], index=1)
st.markdown("#### Hello I am an AI Powered Teacher what shall we learn about today?")

def reset_image_sent_state():
    st.session_state["image_sent_state"] = False

if "upload_file" not in st.session_state:
    st.session_state["upload_file"] = None
st.session_state["upload_file"] = st.sidebar.file_uploader("Choose a document...", type=["jpg", "jpeg", "png", "pdf"], on_change=reset_image_sent_state)

question = st.chat_input("Ask me anything ...")
if question:
    st.markdown(f"*The student has asked me to: {question}*")
    with st.spinner("Please wait a second or two while a I think about that ..."):
        if st.session_state["upload_file"] is None or st.session_state["image_sent_state"]:
            response = st.session_state["session_google"].send_message(question)
        elif st.session_state["upload_file"].type == "application/pdf":
            pdf = st.session_state["upload_file"]
            response = st.session_state["session_google"].send_message([{'mime_type':'application/pdf', 
                                                                       'data': base64.b64encode(pdf.getvalue()).decode('utf-8')}, 
                                                                      question])
        else:
            image = st.session_state["upload_file"]
            base_width = 300
            img = PILImage.open(image)
            wpercent = (base_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            preview_img = img.resize((base_width, hsize), PILImage.Resampling.LANCZOS)
            st.image(preview_img)
            response = st.session_state["session_google"].send_message([{'mime_type':'image/jpeg', 
                                                                       'data': base64.b64encode(image.getvalue()).decode('utf-8')}, 
                                                                      question])
        st.session_state["image_sent_state"] = True
        st.markdown(response.text)