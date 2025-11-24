import requests

BACKEND_URL = "https://intelligent-email-assistant.onrender.com"

def wake_backend():
    try:
        requests.get(f"{BACKEND_URL}/api/wakeup", timeout=2)
    except:
        pass

# INBOX

def get_emails():
    try:
        r = requests.get(f"{BACKEND_URL}/api/emails")
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


def load_mock_inbox():
    try:
        r = requests.post(f"{BACKEND_URL}/api/inbox/load")
        r.raise_for_status()
        return True
    except Exception:
        return False


# PROCESS EMAIL 

def process_email(email_id):
    try:
        r = requests.post(f"{BACKEND_URL}/api/emails/process/{email_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


# PROMPTS 

def get_prompt_templates():
    try:
        r = requests.get(f"{BACKEND_URL}/api/prompts")
        r.raise_for_status()
        return r.json()
    except:
        return []

def update_prompt(prompt_id, payload):
    try:
        r = requests.put(f"{BACKEND_URL}/api/prompts/{prompt_id}", json=payload)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


# AGENT 

def agent_query(payload):
    try:
        r = requests.post(f"{BACKEND_URL}/api/agent/query", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"detail": str(e)}


# DRAFTS

def get_drafts():
    try:
        r = requests.get(f"{BACKEND_URL}/api/drafts")
        r.raise_for_status()
        return r.json()
    except:
        return []





