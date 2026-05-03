# main.py

import os
import uvicorn
from fastapi import FastAPI

from db.base import Base
from db.session import engine
from models.user import Users

from api.routes.auth import router as auth_router
from api.routes.users import router as users_router



app = FastAPI(
    version="1.0.0", 
    title="AuthBase API", 
    description="API de autenticação e gerenciamento de usuários usando FastAPI, SQLAlchemy e JWT."
)


# cria tabelas no startup
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)



if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
