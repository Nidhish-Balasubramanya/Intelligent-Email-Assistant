import streamlit as st
from utils import get_emails, load_mock_inbox, process_email
import datetime as datetime

st.title("📥 Inbox")
st.markdown("### Load and process your inbox emails")

# -------------------------
# LOAD INBOX (Manual Only)
# -------------------------
if st.button("📩 Load Inbox", use_container_width=True):
    ok = load_mock_inbox()
    if ok:
        st.success("Inbox loaded!")
    else:
        st.error("Failed to load inbox.")
    st.rerun()

# -------------------------
# Fetch emails
# -------------------------
emails = get_emails()

if not emails:
    st.info("No emails loaded. Click 'Load Inbox'.")
    st.stop()

# -------------------------
# Process All
# -------------------------
if st.button("⚙ Process All Emails", use_container_width=True):
    progress = st.progress(0)
    total = len(emails)

    for i, email in enumerate(emails):
        process_email(email["id"])
        progress.progress((i + 1) / total)

    st.success("Processing completed!")
    st.rerun()

st.markdown("---")

# -------------------------
# Display Emails
# -------------------------
for email in emails:
    with st.container():
        st.markdown(f"## {email['subject']}")
        st.markdown(f"**From:** {email['sender']}")

        ts = email.get("timestamp")
        if ts:
            dt = datetime.datetime.fromisoformat(ts)
            st.markdown(f"**{dt.strftime('%b %d, %Y %I:%M %p')}**")

        st.write(email["body"][:200] + "...")

        if st.button("View Details", key=email["id"], use_container_width=True):
            st.session_state["selected_email"] = email["id"]
            st.switch_page("pages/2_Email_Viewer.py")

        st.markdown("---")
