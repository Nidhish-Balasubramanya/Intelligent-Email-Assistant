# backend/app/models.py
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.db import Base
from sqlalchemy.orm import relationship
from backend.app.db import Base

def gen_id(prefix=""):
    return f"{prefix}{uuid.uuid4().hex[:8]}"

class Email(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True, index=True)
    sender = Column(String)
    recipient = Column(String)
    subject = Column(String)
    body = Column(Text)
    timestamp = Column(DateTime)
    thread_id = Column(String, nullable=True)

    # FIX: add missing relationship
    processed = relationship(
        "ProcessedEmail",
        back_populates="email",
        cascade="all, delete-orphan",
        uselist=False
    )



class ProcessedEmail(Base):
    __tablename__ = "processed_emails"
    id = Column(String, primary_key=True, default=lambda: gen_id("proc-"))
    email_id = Column(String, ForeignKey("emails.id"), nullable=False, unique=True)
    category = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    action_items = Column(JSON, nullable=True)  # list of objects
    raw_llm_response = Column(Text, nullable=True)
    processed_at = Column(DateTime, default=datetime.utcnow)

    email = relationship("Email", back_populates="processed")

class PromptTemplate(Base):
    __tablename__ = "prompts"
    id = Column(String, primary_key=True, default=lambda: gen_id("prompt-"))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # categorization|action|reply|other
    template = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Draft(Base):
    __tablename__ = "drafts"
    id = Column(String, primary_key=True, default=lambda: gen_id("draft-"))
    email_id = Column(String, ForeignKey("emails.id"), nullable=True)
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    draft_metadata = Column(JSON, nullable=True)  # renamed here
    saved_at = Column(DateTime, default=datetime.utcnow)

    email = relationship("Email", back_populates="drafts")



