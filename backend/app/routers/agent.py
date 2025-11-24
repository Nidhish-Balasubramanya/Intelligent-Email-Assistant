from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app.services.agent_service import handle_agent_query

router = APIRouter()


class AgentRequest(BaseModel):
    email_id: Optional[str] = None
    prompt_type: str  # 'summarize' | 'tasks' | 'reply' | 'custom'
    user_query: str
    tone: Optional[str] = "professional"
    save_draft: Optional[bool] = False


class AgentResponse(BaseModel):
    result_text: str
    parsed_json: Optional[Any] = None
    draft_id: Optional[str] = None


@router.post("/query", response_model=AgentResponse)
def query_agent(payload: AgentRequest, db: Session = Depends(get_db)):
    """
    Advanced agent endpoint. It uses stored prompt templates + processed email metadata.
    Example payload:
    {
      "email_id": "email-01",
      "prompt_type": "reply",
      "user_query": "Draft a friendly reply asking for clarification and propose times",
      "tone": "friendly",
      "save_draft": true
    }
    """
    # Basic validation
    if payload.prompt_type not in ("summarize", "tasks", "reply", "custom"):
        raise HTTPException(status_code=400, detail="Invalid prompt_type. Use summarize|tasks|reply|custom")

    result = handle_agent_query(
        db=db,
        email_id=payload.email_id,
        prompt_type=payload.prompt_type,
        user_query=payload.user_query,
        tone=payload.tone,
        save_draft=payload.save_draft
    )

    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    # Ensure result fields exist for response_model
    return {
        "result_text": result.get("result_text", ""),
        "parsed_json": result.get("parsed_json"),
        "draft_id": result.get("draft_id")
    }


