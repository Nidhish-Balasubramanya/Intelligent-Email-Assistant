from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db import Base, engine
from backend.app.routers import emails, prompts, agent, drafts
from backend.app.seed_prompts import seed_default_prompts
from backend.app.db import SessionLocal
from backend.app.routers import inbox

# Create DB tables (safe for dev)
Base.metadata.create_all(bind=engine)

# Seed default prompts on startup
with SessionLocal() as db:
    seed_default_prompts(db)

app = FastAPI(title="Intelligent Email Assistant - Backend")

app.include_router(inbox.router, prefix="/api/inbox", tags=["inbox"])

# CORS (so Streamlit/dev UI can talk to it)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # narrow this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(emails.router, prefix="/api/emails", tags=["emails"])
app.include_router(prompts.router, prefix="/api/prompts", tags=["prompts"])
app.include_router(agent.router, prefix="/api/agent", tags=["agent"])
app.include_router(drafts.router, prefix="/api/drafts", tags=["drafts"])

# root
@app.get("/")
def root():
    return {"status": "ok", "service": "email-agent-backend"}

@app.get("/api/wakeup")
def wakeup():
    return {"status": "awake"}







