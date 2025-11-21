# backend/app/routers/inbox.py
"""
Loads emails from mock_inbox.json into the database.
This is required to initialize the inbox before processing.
"""

import json
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app import models
import os

router = APIRouter()

# Find absolute path of inbox.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up twice: routers → app → backend
BACKEND_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))

# Path to mock_inbox.json
MOCK_PATH = os.path.join(BACKEND_DIR, "mock_inbox.json")

@router.post("/load")
def load_mock_inbox(db: Session = Depends(get_db)):
    """Load emails from mock_inbox.json into the database."""
    with open(MOCK_PATH, "r", encoding="utf-8") as f:
        inbox_data = json.load(f)

    inserted = 0

    for entry in inbox_data:
        # Convert timestamp string → datetime object
        ts = entry.get("timestamp")
        
        if ts:
            ts = ts.replace("Z", "+00:00")  # convert Zulu time to offset format
            ts = datetime.fromisoformat(ts)
        
        email = models.Email(
            sender=entry["sender"],
            recipient=entry["recipient"],
            subject=entry.get("subject"),
            body=entry.get("body"),
            timestamp=ts
        )
        db.add(email)
        inserted += 1

    db.commit()

    return {"status": "success", "inserted": inserted}




