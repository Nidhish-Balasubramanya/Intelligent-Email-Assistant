from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from backend.app import schemas, models
from backend.app.db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.DraftOut)
def create_draft(payload: schemas.DraftCreate, db: Session = Depends(get_db)):
    d = models.Draft(**payload.dict())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@router.get("/", response_model=List[schemas.DraftOut])
def list_drafts(db: Session = Depends(get_db)):
    return db.query(models.Draft).all()


