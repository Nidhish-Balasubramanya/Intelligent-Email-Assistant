from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.db import get_db
from backend.app import models, schemas
from backend.app.services.processor import process_email


router = APIRouter()

@router.get("/", response_model=list[schemas.EmailOut])
def list_emails(db: Session = Depends(get_db)):
    emails = db.query(models.Email).all()
    processed_map = {
        p.email_id: p for p in db.query(models.ProcessedEmail).all()
    }

    output = []
    for e in emails:
        p = processed_map.get(e.id)

        output.append({
            "id": e.id,
            "sender": e.sender,
            "recipient": e.recipient,
            "subject": e.subject,
            "body": e.body,
            "timestamp": e.timestamp,
            "thread_id": e.thread_id,

            # ADD processed metadata
            "category": p.category if p else None,
            "reason": p.reason if p else None,
            "action_items": p.action_items if p else None
        })

    return output


@router.post("/", response_model=schemas.EmailOut)
def create_email(payload: schemas.EmailCreate, db: Session = Depends(get_db)):
    email = models.Email(**payload.dict())
    db.add(email)
    db.commit()
    db.refresh(email)
    return email

@router.get("/{email_id}", response_model=schemas.EmailOut)
def get_email(email_id: str, db: Session = Depends(get_db)):
    email = db.get(models.Email, email_id)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.post("/process/{email_id}")
def process_single_email(email_id: str, db: Session = Depends(get_db)):
    """
    Run full AI processing on a single email:
    - Categorization
    - Optional action extraction
    """
    return process_email(email_id, db)


