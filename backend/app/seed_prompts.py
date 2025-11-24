from sqlalchemy.orm import Session
from backend.app.models import PromptTemplate


def seed_default_prompts(db: Session):
    """Insert default prompts if they do not exist."""
    
    default_prompts = [
        {
            "name": "Email Categorization",
            "type": "categorization",
            "template": (
                "Please read the email below and assign it to one category:\n"
                "Important, Newsletter, Spam, or To-Do.\n\n"
                "Respond in JSON format like this:\n"
                "{\n"
                "  \"category\": \"<category>\",\n"
                "  \"reason\": \"<short explanation>\"\n"
                "}\n\n"
                "Here is the email:\n"
                "{email_body}"
            )
        },
        {
            "name": "Action Item Extraction",
            "type": "action",
            "template": (
                "Extract actionable items from this email.\n"
                "Return ONLY valid JSON.\n\n"
                "Each item must follow:\n"
                "{\n"
                "  \"task\": \"short description\",\n"
                "  \"deadline\": \"<ISO date or null>\",\n"
                "  \"assignee\": \"<person or null>\"\n"
                "}\n\n"
                "Return array [] if no tasks.\n\n"
                "Email:\n{email_body}\n\n"
                "{user_query}"
            )
        },
        {
            "name": "Draft Reply Generator",
            "type": "reply",
            "template": (
                "You are an email reply assistant.\n"
                "You MUST return ONLY valid JSON.\n"
                "No explanation, no markdown, no extra text.\n\n"
                "Draft a reply using tone: {tone}.\n\n"
                "Return EXACTLY this JSON:\n"
                "{\n"
                "  \"subject\": \"<subject line>\",\n"
                "  \"body\": \"<email body text>\"\n"
                "}\n\n"
                "Email:\n{email_body}\n\n"
                "User instruction:\n{user_query}"
            )
        },
        {
            "name": "Summarization Template",
            "type": "summarize",
            "template": (
                "Summarize the email in 2–3 clear sentences.\n"
                "Return ONLY plain text.\n\n"
                "Email:\n{email_body}\n\n"
                "Instruction:\n{user_query}"
            )
        },
        {
            "name": "Task Extraction (High-Level)",
            "type": "tasks",
            "template": (
                "Extract key tasks from the email.\n"
                "Return ONLY a JSON array of strings.\n"
                "Do NOT include ```json, ``` or any markdown formatting.\n\n"
                "Example:\n"
                "[\"Send the report\", \"Confirm meeting time\"]\n\n"
                "Email:\n{email_body}\n\n"
                "{user_query}"
            )
        }
,
        {
            "name": "Custom Instruction Template",
            "type": "custom",
            "template": (
                "Follow the user's instruction based on the email context.\n\n"
                "Email:\n{email_body}\n\n"
                "Instruction:\n{user_query}"
            )
        }
    ]


    for prompt in default_prompts:
        exists = (
            db.query(PromptTemplate)
            .filter(PromptTemplate.type == prompt["type"])
            .first()
        )
        if not exists:
            db.add(PromptTemplate(**prompt))
    
    db.commit()


