from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from backend.app.services.llm_adapter import GeminiLLM
from backend.app import models
import json

llm = GeminiLLM()

def _get_prompt_by_type(db: Session, prompt_type: str):
    return db.query(models.PromptTemplate).filter(models.PromptTemplate.type == prompt_type).first()

def _build_context(email: Optional[models.Email], processed: Optional[models.ProcessedEmail]) -> str:
    parts = []
    if email:
        parts.append(f"From: {email.sender}\nTo: {email.recipient}\nSubject: {email.subject or ''}\n\n{email.body or ''}")
    if processed:
        parts.append("\n--- Processed Metadata ---")
        parts.append(f"Category: {processed.category}")
        if processed.reason:
            parts.append(f"Reason: {processed.reason}")
        if processed.action_items:
            try:
                ai = json.dumps(processed.action_items, ensure_ascii=False, indent=2)
            except:
                ai = str(processed.action_items)
            parts.append(f"Action items: {ai}")
    return "\n\n".join(parts)

def handle_agent_query(db: Session, email_id: Optional[str], prompt_type: str, user_query: str, tone: Optional[str] = "professional", save_draft: bool = False) -> Dict[str, Any]:
    # If inbox-wide query
    if not email_id or email_id == "__inbox__":
        # Aggregate processed emails to form a context
        processed = db.query(models.ProcessedEmail).all()
        snippets = []
        for p in processed:
            e = db.get(models.Email, p.email_id)
            if e:
                snippets.append(f"Subject: {e.subject}\nCategory: {p.category}\nReason: {p.reason}\nBody: {e.body[:300]}")
        context_text = "\n\n".join(snippets)
        # choose prompt template - use 'custom' or prompt_type mapping
        prompt_template = _get_prompt_by_type(db, prompt_type) or _get_prompt_by_type(db, "custom")
        if not prompt_template:
            return {"error": "No prompt template found for inbox-wide query."}
        filled = prompt_template.template.replace("{email_body}", context_text).replace("{tone}", tone or "professional").replace("{user_query}", user_query or "")
        llm_response = llm.run(filled, temperature=0.2, max_tokens=1200)
        return {"result_text": llm_response, "parsed_json": None}
        
    # Per-email handling
    email = db.get(models.Email, email_id)
    processed = db.query(models.ProcessedEmail).filter(models.ProcessedEmail.email_id == email_id).first()
    prompt_template = _get_prompt_by_type(db, prompt_type)
    if not prompt_template:
        return {"error": f"No prompt template found for type '{prompt_type}'."}
    template = prompt_template.template
    filled = template.replace("{email_body}", _build_context(email, processed) if email or processed else "")
    filled = filled.replace("{tone}", tone or "professional")
    filled = filled.replace("{user_query}", user_query or "")
    llm_response = llm.run(filled, temperature=0.2, max_tokens=800)
    parsed_json = None
    draft_id = None
    
    if prompt_type == "reply":
        try:
            parsed_json = json.loads(llm_response)
        except:
            parsed_json = None
        if parsed_json and ("subject" in parsed_json or "body" in parsed_json) and save_draft:
            # save draft
            draft = models.Draft(email_id=email_id, subject=parsed_json.get("subject"), body=parsed_json.get("body"), draft_metadata={"generated_by":"agent","prompt_type":prompt_type})
            db.add(draft)
            db.commit()
            db.refresh(draft)
            draft_id = draft.id
            
    if prompt_type == "tasks":
        try:
            parsed_json = json.loads(llm_response)
        except:
            parsed_json = None
    return {"result_text": llm_response, "parsed_json": parsed_json, "draft_id": draft_id}


