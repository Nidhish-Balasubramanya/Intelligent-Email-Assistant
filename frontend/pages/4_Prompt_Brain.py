import streamlit as st
from utils import get_prompt_templates, update_prompt

st.title("🧠 Prompt Brain")

prompts = get_prompt_templates()

for p in prompts:
    st.subheader(f"{p['name']} ({p['type']})")

    new_template = st.text_area(f"Template for {p['type']}", p["template"], height=250)

    if st.button(f"Save {p['type']}"):
        update_prompt(p["id"], {
            "name": p["name"],
            "type": p["type"],
            "template": new_template
        })
        st.success("Updated!")
