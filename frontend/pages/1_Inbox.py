import streamlit as st
from utils import get_emails, process_email, load_mock_inbox
import datetime

st.title("📥 Inbox")
st.markdown("### Manage and process your inbox emails with AI.")

# ----------------- LOAD BUTTON -----------------

if st.button("📨 Load Inbox", type="primary"):
    ok = load_mock_inbox()
    if ok:
        st.success("Inbox loaded!")
        st.rerun()
    else:
        st.error("Failed to load inbox. Check backend.")
        st.stop()

# ----------------- FETCH EMAILS -----------------

emails = get_emails()

# No auto-load, no rerun loops.
# If empty, simply show message.
if not emails:
    st.info("No emails found. Click 'Load Inbox' to add sample emails.")
    st.stop()

# ----------------- PROCESS ALL BUTTON -----------------

if st.button("⚙ Process All Emails", use_container_width=True):
    progress = st.progress(0)
    status = st.empty()
    total = len(emails)

    for i, email in enumerate(emails):
        status.write(f"Processing: {email['subject']}")
        try:
            process_email(email["id"])
        except Exception as e:
            status.write(f"Error: {e}")
        progress.progress((i + 1) / total)

    st.success("All emails processed!")
    st.rerun()

st.markdown("---")

CATEGORY_COLORS = {
    "Important": "#ff4d4d",
    "Newsletter": "#4CAF50",
    "Spam": "#9E9E9E",
    "To-Do": "#2196F3",
    "Unknown": "#BDBDBD"
}

# ----------------- DISPLAY EMAILS -----------------

for email in emails:
    with st.container():
        st.markdown(f"## {email['subject']}")
        st.markdown(f"**From:** {email['sender']}")

        ts = email.get("timestamp")
        if ts:
            try:
                dt = datetime.datetime.fromisoformat(ts)
                st.markdown(f"**{dt.strftime('%b %d, %Y %I:%M %p')}**")
            except:
                st.markdown(f"**{ts}**")

        st.write(email["body"][:200] + "...")

        cat = email.get("category") or "Not processed"
        color = CATEGORY_COLORS.get(cat, "#555")
        st.markdown(
            f"<span style='background:{color}; padding:6px 12px; border-radius:8px; "
            f"color:white; font-size:0.9rem;'>{cat}</span>",
            unsafe_allow_html=True
        )

        if st.button("View Details", key=email["id"], use_container_width=True):
            st.session_state["selected_email"] = email["id"]
            st.switch_page("pages/2_Email_Viewer.py")

        st.markdown("---")
