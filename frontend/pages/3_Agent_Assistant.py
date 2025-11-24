import streamlit as st
from utils import get_emails, agent_query

st.title("🤖 AI Agent Assistant")

emails = get_emails()
# add a special entry for entire inbox
options = ["-- Entire Inbox --"] + [e["subject"] for e in emails]
choice = st.selectbox("Select an email:", options)
email_id = None if choice == "-- Entire Inbox --" else next((e["id"] for e in emails if e["subject"] == choice), None)

action = st.radio("Action", ["Summarize", "Tasks", "Draft Reply", "Custom"])

# instruction defaulting mechanism without session_state conflicts
if "last_action" not in st.session_state:
    st.session_state.last_action = action

if st.session_state.last_action != action:
    st.session_state["instr"] = ""

    # Clear previous results when switching action
    if "agent_result" in st.session_state:
        del st.session_state["agent_result"]

    st.session_state.last_action = action


default = ""
if action == "Summarize":
    default = "Summarize the email in 2–3 sentences."
elif action == "Tasks":
    default = "Extract the key tasks from this email."
elif action == "Draft Reply":
    default = "Create a polite reply and include a subject."
else:
    default = ""

if st.session_state.get("instr","") == "":
    st.session_state["instr"] = default

instr = st.text_area("Instruction", key="instr")

if st.button("Run Agent"):
    mapped_type = action.lower().replace(" ", "")
    if mapped_type == "draftreply":
        mapped_type = "reply"
    payload = {
        "email_id": email_id if email_id else "__inbox__",
        "prompt_type": mapped_type,
        "user_query": instr,
        "tone": "professional",
        "save_draft": (mapped_type == "reply")
    }
    result = agent_query(payload)
    st.session_state["agent_result"] = result

if "agent_result" in st.session_state:
    res = st.session_state["agent_result"]
    st.markdown("---")
    if "detail" in res:
        st.error(res["detail"])
    else:
        st.markdown("### Result")
        # Summarize
        if action == "Summarize":
            st.write(res.get("result_text"))
        elif action == "Tasks":
            parsed = res.get("parsed_json")
            if parsed:
                for t in parsed:
                    st.checkbox(t, key=f"task_{t}")
            else:
                # fallback if result_text contains JSON array string
                st.write(res.get("result_text"))
        elif action == "Draft Reply":
            parsed = res.get("parsed_json")

            # Fix: handle list OR dict safely
            if isinstance(parsed, list) and len(parsed) > 0:
                parsed = parsed[0]   # extract first element

            if isinstance(parsed, dict):
                subject = parsed.get("subject", "(No subject)")
                body = parsed.get("body", "(No body)")

                st.markdown(f"**Subject:** {subject}")
                st.write(body)

                if res.get("draft_id"):
                    st.success(f"Draft saved (ID: {res.get('draft_id')})")
            else:
                st.warning("LLM returned unexpected format. Showing raw output:")
                st.write(res.get("result_text"))

        else:
            st.write(res.get("result_text"))

