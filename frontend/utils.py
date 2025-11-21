# frontend/utils.py
import requests
BASE_URL = "https://intelligent-email-assistant.onrender.com"

def get_emails():
    try:
        r = requests.get(f"{BASE_URL}/emails")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return []

def process_email(email_id):
    try:
        r = requests.post(f"{BASE_URL}/emails/process/{email_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"detail": str(e)}

def get_prompt_templates():
    try:
        r = requests.get(f"{BASE_URL}/prompts")
        r.raise_for_status()
        return r.json()
    except:
        return []

def update_prompt(prompt_id, payload):
    try:
        r = requests.put(f"{BASE_URL}/prompts/{prompt_id}", json=payload)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"detail": str(e)}

def agent_query(payload):
    try:
        r = requests.post(f"{BASE_URL}/agent/query", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"detail": str(e)}

def get_drafts():
    try:
        r = requests.get(f"{BASE_URL}/drafts")
        r.raise_for_status()
        return r.json()
    except:
        return []

