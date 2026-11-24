
import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
load_dotenv()

# Connect to OpenAI
api_key = os.getenv("OPENAI_API_KEY")

# Website settings
st.set_page_config(
    page_title="NOVA AI",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 NOVA AI")
st.caption("Your Personal AI Assistant")

# Check API key
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

client = OpenAI(api_key=api_key)

# Store conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask NOVA anything...")

if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("NOVA is thinking..."):

            try:
                response = client.responses.create(
                    model="gpt-5.5",
                    instructions=(
                        "You are NOVA, a helpful and friendly "
                        "AI assistant. Explain things clearly."
                    ),
                    input=st.session_state.messages
                )

                answer = response.output_text
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")