import streamlit as st

st.set_page_config(
    page_title="OceanAI Email Agent",
    page_icon="📨",
    layout="wide"
)

st.title("📨 OceanAI – Intelligent Email Assistant")
st.markdown("""
Welcome to **OceanAI Email Agent**, your intelligent companion for email classification, task extraction, and automated reply drafting.

### 🔧 Features
- 📥 Load & view inbox emails  
- 🧠 Automatic categorization & action item extraction  
- 🤖 AI Agent for summaries, tasks, replies & custom queries  
- 📝 Draft reply generation + storage  
- 🔏 Fully editable Prompt Brain  
- ⚙ Built with FastAPI + Streamlit + Gemini

Use the sidebar to navigate through the application.
""")
