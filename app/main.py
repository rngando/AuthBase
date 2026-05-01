# main.py

from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.models.user import Users

from app.api.routes.auth import router as auth_router

app = FastAPI(title="AuthBase API", version="1.0.0")

# cria tabelas no startup
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)