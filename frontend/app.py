import streamlit as st
from utils import wake_backend
st.set_page_config(
    page_title="Email Agent",
    page_icon="📨",
    layout="wide"
)

st.title("Intelligent Email Assistant")
st.markdown("""
Welcome to **IEA**, your intelligent companion for email classification, task extraction, and automated reply drafting.

###  Features
- 📥 Load & view inbox emails  
- 🧠 Automatic categorization & action item extraction  
- 🤖 AI Agent for summaries, tasks, replies & custom queries  
- 📝 Draft reply generation + storage  
- 🔏 Fully editable Prompt Brain  
- ⚙ Built with FastAPI + Streamlit + Gemini

Use the sidebar to navigate through the application.

Before using the application please warm up the backend by clicking on the below link and waiting for 2-3mins.

[warm up the backend](https://intelligent-email-assistant.onrender.com)
""")









