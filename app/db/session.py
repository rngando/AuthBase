# app/db/session.py

from app.core.config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

