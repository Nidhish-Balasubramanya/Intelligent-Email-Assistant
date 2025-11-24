import streamlit as st
from utils import get_emails, load_mock_inbox, process_email
import datetime as datetime

st.title("📥 Inbox")
st.markdown("### Load and process your inbox emails")

# LOAD INBOX
if st.button("📩 Load Inbox", use_container_width=True):
    ok = load_mock_inbox()
    if ok:
        st.success("Inbox loaded!")
    else:
        st.error("Failed to load inbox.")
    st.rerun()

# Fetch emails
emails = get_emails()

if not emails:
    st.info("No emails loaded. Click 'Load Inbox'.")
    st.stop()

#'Process All' Button 
if st.button("⚙ Process All Emails", use_container_width=True):
    progress = st.progress(0)
    status = st.empty()

    total = len(emails)

    for i, email in enumerate(emails):
        status.write(f"Processing: {email['subject']}")
        try:
            process_email(email["id"])
        except Exception as e:
            status.write(f"Error processing {email['subject']}: {e}")

        progress.progress((i + 1) / total)

    st.success("All emails processed successfully!")
    st.rerun()

st.markdown("---")

# Category badge colors
CATEGORY_COLORS = {
    "Important": "#ff4d4d",
    "Newsletter": "#4CAF50",
    "Spam": "#9E9E9E",
    "To-Do": "#2196F3",
    "Unknown": "#BDBDBD"
}

# Display email list
for email in emails:
    with st.container():
        st.markdown(f"## {email['subject']}")

        st.markdown(f"**From:** {email['sender']}")

        ts = email.get("timestamp")
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                st.markdown(f"**{dt.strftime('%b %d, %Y %I:%M %p')}**")
            except:
                st.markdown(f"**{ts}**")

        st.write(email["body"][:180] + "...")

        # Category tag
        if email.get("category"):
            color = CATEGORY_COLORS.get(email["category"], "#444")
            st.markdown(
                f"<span style='background:{color}; padding:6px 12px; "
                f"border-radius:8px; color:white; font-size:0.9rem;'>"
                f"{email['category']}</span>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<span style='background:#555; padding:6px 12px; "
                "border-radius:8px; color:white; font-size:0.9rem;'>Not processed</span>",
                unsafe_allow_html=True
            )

        st.write("")  # spacing

        # Single 'View Details' button
        if st.button("View Details", key=email["id"], use_container_width=True):
            st.session_state["selected_email"] = email["id"]
            st.switch_page("pages/2_Email_Viewer.py")

        st.markdown("---")

