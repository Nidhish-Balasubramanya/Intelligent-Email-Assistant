# Prompt-Driven Email Productivity Agent

A full-stack AI system that ingests emails, categorizes them, extracts
action items, supports inbox reasoning, and generates draft replies
using customizable prompts.

## 1. Project Overview
This project implements a Prompt-Driven Email Productivity Agent that automates email understanding and assists users with inbox management. The system loads emails (mock or real), processes them using customizable LLM prompt templates, and provides intelligent features such as categorization, action extraction, summarization, email drafting, and inbox-wide reasoning.

The architecture is modular:  
- The backend manages emails, processing pipelines, prompt configurations, and drafts.  
- The frontend provides an interactive UI that enables users to load emails, process them, view details, interact with the agent, and manage prompts.

This project is designed to satisfy all functional requirements defined in the assignment specification.

---

## 2. Features

### Phase 1: Email Ingestion & Prompt Storage
- Load emails from mock JSON file or email provider (extensible).
- View emails with sender, subject, timestamp, preview, and category tags.
- Full prompt management panel:
  - Categorization Prompt
  - Action Item Extraction Prompt
  - Draft Reply Prompt
  - Additional task/summarization/custom prompts
- All prompts stored in DB for persistence.
- Email processing pipeline:
  - Run categorization LLM prompt  
  - Run action-item extraction LLM prompt  
  - Persist results in database  
  - Show badges in UI

### Phase 2: AI Email Agent
- Select any email to interact with.
- Ask the agent:
  - “Summarize this email”
  - “What tasks do I need to do?”
  - “Draft a reply in a specific tone”
  - General inbox questions like “Show me urgent emails”
- Supports inbox-wide reasoning (no email selected).
- Uses prompt templates + user instruction + email context.

### Phase 3: Draft Generation Agent
- Generate new email drafts.
- Reply to emails using auto-reply template.
- Edit and save drafts.
- Drafts stored in DB with metadata.

### Additional Features
- Mock inbox auto-loader on first run.
- Process-all-emails button with progress feedback.
- Clean viewer for email details and processed information.
- Streamlined agent interface with action-specific instructions.
- Robust JSON parsing with fallback handling.
- Gemini LLM integration via adapters.

---

##  3. Setup Instructions

### 3.1 Clone Repository

    git clone <your-repo-url>
    cd OceanAI

### 3.2 Create Virtual Environment

    python -m venv venv
    source venv/bin/activate   # Windows: venv\Scripts\activate

### 3.3 Install Dependencies

    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt

### 3.4 Set Environment Variables

Create `.env` inside **backend/**:

    GEMINI_API_KEY=your_key_here
    DATABASE_URL=sqlite:///./emails.db

------------------------------------------------------------------------

##  4. How to Run the Backend (FastAPI)

### Start Backend Server

    cd backend
    uvicorn app.main:app --reload --port 7000

Backend will run at:\
👉 **http://localhost:7000**

------------------------------------------------------------------------

## 5. How to Run the UI (Streamlit)

### Start Frontend

    cd frontend
    streamlit run app.py

Frontend will run at:\
👉 **http://localhost:8501**

------------------------------------------------------------------------

## 6. How to Load the Mock Inbox

On first launch: - The UI automatically checks if emails exist. - If
empty, it will load **mock_emails.json** from the backend.

Manual loading (via API):

    POST /api/inbox/load

From UI: - Go to **Inbox** page\
- Click **Load Mock Inbox** (if shown)

------------------------------------------------------------------------

## 7. How to Configure Prompts

Navigate to **Prompts Panel** in the Streamlit sidebar.

Editable prompt templates: - Categorization Prompt\
- Action Item Extraction Prompt\
- Draft Reply Prompt\
- Summarization Prompt\
- Custom Query Prompt

Each template supports variables such as:

    {email_body}
    {user_query}
    {tone}

Prompts are stored in the database and persist across restarts.

------------------------------------------------------------------------

## 8. Usage Examples

### 🔹 8.1 Categorize & Extract Actions From All Emails

UI → Inbox → **Process All Emails**

Backend API:

    POST /api/emails/process/{email_id}

### 🔹 8.2 Summarize an Email

Agent Page → Select Email → Ask:

    "Summarize this email."

### 🔹 8.3 Get Action Items

    "What tasks do I need to complete?"

### 🔹 8.4 Generate a Draft Reply

    "Draft a polite reply thanking them and accepting the offer."

### 🔹 8.5 Inbox‑Wide Query (No Email Selected)

    "Show me all urgent emails."

------------------------------------------------------------------------

## 9. System Architecture

### Components
- Frontend: Streamlit  
- Backend: FastAPI  
- Database: SQLite (local) / PostgreSQL (production)  
- LLM: Gemini (via Google Generative AI SDK)

### Data Flow
1. Emails loaded into DB → frontend displays inbox.  
2. User triggers email processing → backend runs LLM prompts → saves processed metadata.  
3. Agent queries (summarize, tasks, reply) sent from UI → backend → LLM → results returned.  
4. Draft replies stored in database and viewable in UI.

---

## 10. Tech Stack

### Frontend
- Streamlit  
- Python requests  
- Session state management

### Backend
- FastAPI  
- Uvicorn  
- SQLAlchemy ORM  
- Pydantic models  
- PostgreSQL / SQLite  
- Google Generative AI SDK (Gemini LLM)

### Tools
- Railway deployment  
- Docker-compatible project layout  

---

## 11. Folder Structure
```
intelligent-email-assistant/
│
├── backend/
│   ├── app/
│   │   ├── __pycache__/
│   │   │
│   │   ├── routers/
│   │   │   ├── __pycache__/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── drafts.py
│   │   │   ├── emails.py
│   │   │   ├── health.py
│   │   │   ├── inbox.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── services/
│   │   │   ├── __pycache__/
│   │   │   ├── agent_service.py
│   │   │   ├── llm_adapter.py
│   │   │   ├── processor.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── main.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── seed_prompts.py
│   │   ├── email_agent.db
│   │   ├── mock_inbox.json
│   │   └── test.py
│   │
│   └── requirements.txt
│
│
├── frontend/
│   ├── __pycache__/
│   │
│   ├── pages/
│   │   ├── 1_Inbox.py
│   │   ├── 2_Email_Viewer.py
│   │   ├── 3_Agent_Assistant.py
│   │   ├── 4_Prompt_Brain.py
│   │   └── 5_Draft_Manager.py
│   │
│   ├── app.py
│   ├── utils.py
│   └── requirements.txt
│
│
├── venv/
│
└── .env

```

---

## 12. Backend (FastAPI)

### Responsibilities
- Email ingestion  
- Email processing (categorization + action extraction)  
- LLM orchestration  
- Prompt storage and editing  
- Draft generation and persistence  

### Core Backend Files
- `main.py` — App entry point  
- `db.py` — SQLAlchemy config  
- `models.py` — ORM models  
- `schemas.py` — Pydantic models  
- `routers/*.py` — API endpoints  
- `services/agent_service.py` — Agent logic  
- `services/llm_adapter.py` — Gemini interface

---

## 13. Frontend (Streamlit)

### Pages
1. Inbox  
2. Email Viewer  
3. Agent Assistant  

### Capabilities
- View and process emails  
- Display metadata (category, reason, actions)  
- Run agent instructions  
- Generate draft replies  
- Navigate between pages  

---

## 14. Database Schema

### Email Table
- id  
- sender  
- recipient  
- subject  
- body  
- timestamp  
- thread_id  

### ProcessedEmail Table
- id  
- email_id  
- category  
- reason  
- action_items (JSON)  
- processed_at  

### PromptTemplate Table
- id  
- name  
- type  
- template  

### Draft Table
- id  
- email_id  
- subject  
- body  
- metadata  

---

## 15. LLM Prompt System
Each prompt stored in DB and used dynamically:
- Categorization  
- Action item extraction  
- Draft reply  
- Summarization  
- High-level task extraction  
- Custom queries  

Supported variables:
- {email_body}  
- {user_query}  
- {tone}  

---

## 16 API Endpoints

### Inbox
- POST `/api/inbox/load`  
- GET `/api/emails`  
- POST `/api/emails/process/{email_id}`  

### Prompts
- GET `/api/prompts`  
- PUT `/api/prompts/{id}`  

### Agent
- POST `/api/agent/query`  

### Drafts
- GET `/api/drafts`  

### Admin
- POST `/api/admin/reset`  
---


## 17 Future Enhancements
- Gmail API ingestion  
- OAuth authentication  
- Attachment parsing  
- Calendar integration  
- Thread reconstruction  
- LLM model switching  
- Email scheduling  

---


