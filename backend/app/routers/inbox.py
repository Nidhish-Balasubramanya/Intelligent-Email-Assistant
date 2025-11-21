import json
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import exists
from backend.app.db import get_db
from backend.app import models
import os

router = APIRouter()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MOCK_PATH = os.path.join(BACKEND_DIR, "mock_inbox.json")

@router.post("/load")
def load_mock_inbox(db: Session = Depends(get_db)):
    """Insert emails from mock_inbox.json, but skip if ID already exists."""
    with open(MOCK_PATH, "r", encoding="utf-8") as f:
        inbox_data = json.load(f)

    inserted = 0

    for entry in inbox_data:
        email_id = entry["id"]  # <- Must exist in JSON

        # Skip if already exists
        exists_q = db.query(exists().where(models.Email.id == email_id)).scalar()
        if exists_q:
            continue

        ts = entry.get("timestamp")
        if ts:
            ts = ts.replace("Z", "+00:00")
            ts = datetime.fromisoformat(ts)

        email = models.Email(
            id=email_id,
            sender=entry["sender"],
            recipient=entry["recipient"],
            subject=entry["subject"],
            body=entry["body"],
            timestamp=ts
        )

        db.add(email)
        inserted += 1

    db.commit()
    return {"status": "success", "inserted": inserted}
