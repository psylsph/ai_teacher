import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(layout="wide")
st.sidebar.header("Configuration")
agent = st.sidebar.selectbox("Select AI Agent:", options=["gemini-1.5-flash-8b-001", "gemini-1.5-flash-002", "gemini-2.0-flash-exp"], index=1)
st.markdown("### AI-Powered Teaching Assistant")
question = st.sidebar.text_input("Enter your question here:")
if st.sidebar.button("Ask AI"):
    with st.spinner("Searching and thinking, please wait..."):
        GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyBud2LfN_RDdqpWGrlfwnR7Ya86Jo32Iag")
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(agent)
        teacher = "Please act as an experienced secondary school teacher with expertise in the subject matter of the question. When I present questions: \n1. First break down the key concepts and principles involved \n2. Provide relatable real-world examples to illustrate each concept \n3. Guide me through the problem-solving approach using the Socratic method \n4. Include practice problems similar to but different from my original question \n5. Only provide the actual answer when I explicitly request it with 'Please show the solution' Please adjust the complexity of your explanations for a secondary school student (ages 14-18) and use clear, engaging language. Feel free to use diagrams or visual explanations when helpful."
        #response = model.generate_content([{'mime_type':'image/png', 'data': image_data}, sentiment_agent_response, content])
        response = model.generate_content([teacher, question])
        st.markdown(response.text)
