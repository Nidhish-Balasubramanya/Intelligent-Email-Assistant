# Prompt-Driven Email Productivity Agent  
A full-stack AI-powered system that ingests emails, categorizes them, extracts actionable items, assists users with summarization and task queries, and generates draft replies based on customizable prompts.  
Built using Streamlit (frontend), FastAPI (backend), PostgreSQL/SQLite (database), and Gemini LLM (LLM engine).

---

## Table of Contents
1. Project Overview  
2. Features  
3. System Architecture  
4. Tech Stack  
5. Folder Structure  
6. Backend (FastAPI)  
7. Frontend (Streamlit)  
8. Database Schema  
9. LLM Prompt System  
10. API Endpoints  
11. Running Locally  
12. Deployment Guide  
13. Future Enhancements  

---

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

## 3. System Architecture

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

## 4. Tech Stack

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

## 5. Folder Structure
```
OceanAI/
│
│── backend/
│     ├── app/
│     │     ├── main.py
│     │     ├── db.py
│     │     ├── models.py
│     │     ├── schemas.py
│     │     ├── seed_prompts.py
│     │     ├── services/
│     │     └── routers/
│     └── requirements.txt
│
│── frontend/
│     ├── app.py
│     ├── utils.py
│     └── pages/
│           ├── 1_Inbox.py
│           ├── 2_Email_Viewer.py
│           └── 3_Agent_Assistant.py
│
└── README.md
```

---

## 6. Backend (FastAPI)

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

## 7. Frontend (Streamlit)

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

## 8. Database Schema

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

## 9. LLM Prompt System
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

## 10. API Endpoints

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

## 11. Running Locally

### Create virtual environment
```
python -m venv venv
source venv/bin/activate  
```

### Install dependencies
```
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### Start Backend
```
uvicorn app.main:app --reload --port 7000
```

### Start Frontend
```
streamlit run frontend/app.py
```

---

## 12. Deployment Guide

### Recommended Deployment: Railway  
Deploy backend, frontend, and Postgres database on Railway.

Steps:
1. Push project to GitHub  
2. Create Railway project  
3. Add Postgres plugin  
4. Deploy backend service from `backend/`  
5. Deploy frontend service from `frontend/`  
6. Set required environment variables  
7. Redeploy and access public URLs  

---

## 13. Future Enhancements
- Gmail API ingestion  
- OAuth authentication  
- Attachment parsing  
- Calendar integration  
- Thread reconstruction  
- LLM model switching  
- Email scheduling  

---

