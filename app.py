
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Configure webpage
st.set_page_config(
    page_title="AI Health Assistant",
    page_icon="🩺"
)

st.title("🩺 Health Assistant")
st.caption("Powered by Groq")

# Check API key
if not api_key:
    st.error("API key is missing. Please configure it.")
    st.stop()

# Connect to Groq
client = Groq(api_key=api_key)

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a general health information assistant. "
                "Provide educational information only. "
                "Do not diagnose, prescribe medicines, or replace "
                "a qualified healthcare professional. "
                "For emergencies, advise immediate medical care."
            )
        }
    ]

# Display previous messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# User input
question = st.chat_input("Ask a health-related question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages,
                temperature=0.3
            )

            answer = response.choices[0].message.content
            st.write(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error("Actual Error:")
            st.exception(e)

# Health disclaimer
st.warning(
    "This application provides general health information, "
    "not medical diagnosis or treatment."
)
