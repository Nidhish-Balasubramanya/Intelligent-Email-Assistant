# backend/app/routers/inbox.py
import json
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db import get_db
from backend.app import models
import os
from dateutil import parser

router = APIRouter()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
MOCK_PATH = os.path.join(BACKEND_DIR, "mock_inbox.json")


@router.get("")
def get_inbox(db: Session = Depends(get_db)):
    emails = db.query(models.Email).all()
    return emails


@router.post("/load")
def load_mock_inbox(db: Session = Depends(get_db)):
    """
    Idempotent loader:
    - Reads mock_inbox.json
    - Skips records already in DB (using sender+subject+timestamp as dedupe key)
    - Inserts only new records
    """
    with open(MOCK_PATH, "r", encoding="utf-8") as f:
        inbox_data = json.load(f)

    # Build set of existing keys for fast lookup
    existing_keys = set()
    for e in db.query(models.Email.sender, models.Email.subject, models.Email.timestamp).all():
        # e is a tuple (sender, subject, timestamp)
        # normalize timestamp to iso string if datetime
        sender, subject, ts = e
        ts_key = ts.isoformat() if hasattr(ts, "isoformat") else (ts or "")
        existing_keys.add((sender or "", subject or "", ts_key))

    inserted = 0
    skipped = 0

    for entry in inbox_data:
        sender = entry.get("sender") or ""
        subject = entry.get("subject") or ""
        ts_str = entry.get("timestamp") or None

        # robust timestamp parsing
        ts = None
        if ts_str:
            try:
                ts = parser.isoparse(ts_str)
            except Exception:
                # fallback: keep raw string as-is (will insert as null or string depending on model)
                ts = None

        ts_key = ts.isoformat() if ts is not None else (ts_str or "")

        key = (sender, subject, ts_key)
        if key in existing_keys:
            skipped += 1
            continue

        # Create and add
        email = models.Email(
            sender=sender,
            recipient=entry.get("recipient"),
            subject=subject,
            body=entry.get("body"),
            timestamp=ts
        )
        db.add(email)
        existing_keys.add(key)
        inserted += 1

    if inserted > 0:
        db.commit()
    else:
        # no new rows to commit; ensure session clean
        db.rollback()

    return {"status": "done", "inserted": inserted, "skipped": skipped}
