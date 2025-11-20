import streamlit as st
from utils import get_drafts

st.title("✉ Draft Manager")

drafts = get_drafts()

if not drafts:
    st.info("No drafts available.")
else:
    for d in drafts:
        st.subheader(d.get("subject", "No Subject"))
        st.text_area("Body", d.get("body", ""), height=200)
        st.markdown("---")
