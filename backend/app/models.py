# backend/app/db.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Read DATABASE_URL from Render environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Render PostgreSQL URLs start with postgres:// (SQLAlchemy requires postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# Create engine for PostgreSQL
engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

Base = declarative_base()

# Dependency used by API routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
