# backend/app/schemas.py
from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime

class EmailCreate(BaseModel):
    sender: str
    recipient: str
    subject: Optional[str]
    body: Optional[str]
    timestamp: Optional[datetime]
    thread_id: Optional[str]

class EmailOut(BaseModel):
    id: str
    sender: str
    recipient: str
    subject: str
    body: str
    timestamp: datetime | None = None
    thread_id: str | None = None

    # New processed fields
    category: str | None = None
    reason: str | None = None
    action_items: dict | list | None = None

    class Config:
        from_attributes = True
        orm_mode = True

class PromptCreate(BaseModel):
    name: str
    type: str
    template: str

class PromptOut(BaseModel):
    id: str
    name: str
    type: str
    template: str

    class Config:
        orm_mode = True

class DraftCreate(BaseModel):
    email_id: Optional[str]
    subject: Optional[str]
    body: Optional[str]
    draft_metadata: Optional[Any]

class DraftOut(BaseModel):
    id: str
    email_id: Optional[str]
    subject: Optional[str]
    body: Optional[str]
    draft_metadata: Optional[Any]

    class Config:
        orm_mode = True
