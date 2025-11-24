from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.db import get_db
from backend.app import models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.PromptOut])
def list_prompts(db: Session = Depends(get_db)):
    """Return all saved prompt templates."""
    return db.query(models.PromptTemplate).all()


@router.post("/", response_model=schemas.PromptOut)
def create_prompt(payload: schemas.PromptCreate, db: Session = Depends(get_db)):
    """Create a new prompt template."""
    prompt = models.PromptTemplate(**payload.dict())
    db.add(prompt)
    db.commit()
    db.refresh(prompt)
    return prompt


@router.get("/{prompt_id}", response_model=schemas.PromptOut)
def get_prompt(prompt_id: str, db: Session = Depends(get_db)):
    """Fetch a single prompt template by ID."""
    prompt = db.get(models.PromptTemplate, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.put("/{prompt_id}", response_model=schemas.PromptOut)
def update_prompt(prompt_id: str, payload: schemas.PromptCreate, db: Session = Depends(get_db)):
    """Update an existing prompt."""
    prompt = db.get(models.PromptTemplate, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    prompt.name = payload.name
    prompt.type = payload.type
    prompt.template = payload.template

    db.commit()
    db.refresh(prompt)
    return prompt


@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: str, db: Session = Depends(get_db)):
    """Delete a prompt template."""
    prompt = db.get(models.PromptTemplate, prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    db.delete(prompt)
    db.commit()
    return {"status": "deleted", "id": prompt_id}


