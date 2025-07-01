import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import html 

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit config
st.set_page_config(page_title="Simple Chatbot", page_icon="🧑🏻‍💻⚙️💬")
st.title(" 🧑🏻‍💻💬Gemini Chatbot")

# Chat history setup
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: clear button
with st.sidebar:
    st.subheader("⚙️ Options")
    if st.button("🧹 Clear all Chats"):
        st.session_state.chat_history = []

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = model.generate_content(user_input)
            answer = response.text

            st.session_state.chat_history.append({
                "question": user_input,
                "answer": answer
            })
        except Exception as e:
            st.error(f"⚠️ Gemini Error: {e}")

# Chat history render (user right, bot left)
for entry in st.session_state.chat_history:
    question = html.escape(entry.get("question", ""))
    answer = html.escape(entry.get("answer", ""))  # ✅ Fix weird </div>

    # User message (right)
    st.markdown(
        f"""
        <div style='display: flex; justify-content: flex-end; margin-bottom: 8px;'>
            <div style='background-color: #DCF8C6; padding: 10px 15px; border-radius: 12px; max-width: 70%; text-align: right; font-family: sans-serif;'>
                {question}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Gemini reply (left)
    st.markdown(
        f"""
        <div style='display: flex; justify-content: flex-start; margin-bottom: 16px;'>
            <div style='background-color: #F1F0F0; padding: 10px 15px; border-radius: 12px; max-width: 70%; font-family: sans-serif;'>
                {answer}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )
