import streamlit as st
from utils import get_emails, process_email

st.title("📄 Email Viewer")

if "selected_email" not in st.session_state:
    st.error("No email selected!")
    st.stop()

email_id = st.session_state["selected_email"]

emails = get_emails()
email = next((e for e in emails if e["id"] == email_id), None)

if not email:
    st.error("Email not found.")
    st.stop()

# UI Layout
st.markdown(f"## {email['subject']}")
st.markdown(f"**From:** {email['sender']}")

# Category Badge 
CATEGORY_COLORS = {
    "Important": "#d9534f",
    "Newsletter": "#5cb85c",
    "Spam": "#999999",
    "To-Do": "#0275d8",
    "Unknown": "#777777"
}

if email.get("category"):
    color = CATEGORY_COLORS.get(email["category"], "#444")
    st.markdown(
        f"<span style='background:{color}; padding:6px 12px; border-radius:6px; color:white;'>"
        f"{email['category']}</span>",
        unsafe_allow_html=True
    )

st.markdown("---")
st.markdown("### 📧 Email Body")
st.write(email["body"])

st.markdown("---")
st.markdown("### 🧠 AI Processing")
# If already processed (category present and not None), show processed data
if email.get("category") is not None:
    st.markdown(f"**Category:** {email.get('category')}")
    st.markdown("**Reason:**")
    # Reason may be plain text or a JSON-ish string; show safely
    reason = email.get("reason")
    if reason:
        # If reason looks like JSON (starts with { ), show as code
        if isinstance(reason, str) and reason.strip().startswith("{"):
            st.code(reason, language="json")
        else:
            st.write(reason)
    else:
        st.write("-")

    st.markdown("**Action items:**")
    action_items = email.get("action_items")
    if action_items:
        # action_items probably is a list or parsed JSON; render nicely
        try:
            st.json(action_items)
        except Exception:
            st.write(action_items)
    else:
        st.write("No action items found.")
else:
    # not processed yet - show Process button
    if st.button("⚙ Process Email", use_container_width=True):
        result = process_email(email_id)
        st.session_state["processing_result"] = result
        st.rerun()


