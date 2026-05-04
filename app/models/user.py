# app/models/user.py

from app.db.base import Base

from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Boolean, DateTime



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)

    # Dados Basicos
    name = Column(String(100), nullable=False)
    email = Column(String(250), nullable=False, unique=True, index=True)

    # Segurança
    hashed_password = Column(String, nullable=False)

    # Permissões
    role = Column(String(50), nullable=False, default="user") # "admin" ou "user"

    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))
