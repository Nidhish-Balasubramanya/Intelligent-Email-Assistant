"""
This module contains the main email processing pipeline.
It uses stored prompt templates + Gemini LLM to:
1. Categorize an email
2. Extract action items (if needed)
3. Store results in the ProcessedEmail table
"""

from sqlalchemy.orm import Session
from backend.app.models import Email, ProcessedEmail, PromptTemplate
from backend.app.services.llm_adapter import GeminiLLM
import json

llm = GeminiLLM()


def apply_prompt(template: str, variables: dict) -> str:
    """Fills placeholders like {email_body} in the template."""
    text = template
    for key, value in variables.items():
        text = text.replace(f"{{{key}}}", value)
    return text


def safe_json_parse(response_text: str):
    """
    Try parsing text to JSON.
    If AI returns extra text around JSON, extract best JSON.
    """
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Attempt to find first {...} block
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(response_text[start:end])
            except:
                return None
        return None


def process_email(email_id: str, db: Session):
    """Runs categorization + action extraction on a single email."""

    email = db.get(Email, email_id)
    if not email:
        return {"error": "Email not found"}

    # Step 1: Get categorization prompt
    cat_prompt = (
        db.query(PromptTemplate)
        .filter(PromptTemplate.type == "categorization")
        .first()
    )

    if not cat_prompt:
        return {"error": "Categorization prompt missing"}

    # Fill template
    filled = apply_prompt(cat_prompt.template, {
        "email_body": email.body or ""
    })

    # Call Gemini
    llm_response = llm.run(filled)
    parsed = safe_json_parse(llm_response)

    if parsed is None:
        parsed = {"category": "Unknown", "reason": "Could not parse AI response"}

    category = parsed.get("category", "Unknown")
    reason = parsed.get("reason", "")

    # Step 2: If To-Do → extract action items
    action_items = None
    if category.lower() in ["to-do", "todo", "task", "action required"]:
        action_prompt = (
            db.query(PromptTemplate)
            .filter(PromptTemplate.type == "action")
            .first()
        )

        if action_prompt:
            filled_action = apply_prompt(action_prompt.template, {
                "email_body": email.body or ""
            })

            act_response = llm.run(filled_action)
            action_items = safe_json_parse(act_response)

    # Step 3: Save results to DB — update if exists
    existing = db.query(ProcessedEmail).filter(ProcessedEmail.email_id == email.id).first()

    if existing:
        existing.category = category
        existing.reason = reason
        existing.action_items = action_items
        existing.raw_llm_response = llm_response
        db.commit()
        db.refresh(existing)
        return {
            "email_id": email.id,
            "category": category,
            "reason": reason,
            "action_items": action_items
        }

    # Otherwise insert a new processed record
    processed = ProcessedEmail(
        email_id=email.id,
        category=category,
        reason=reason,
        action_items=action_items,
        raw_llm_response=llm_response
    )

    db.add(processed)
    db.commit()
    db.refresh(processed)


    return {
        "email_id": email.id,
        "category": category,
        "reason": reason,
        "action_items": action_items
    }


