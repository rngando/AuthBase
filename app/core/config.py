# config.py

import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    PORT = os.getenv("PORT")
    HOST = os.getenv("HOST")
    DB_NAME = os.getenv("DB_NAME")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    DATABASE_URL = f"sqlite:///{DB_NAME}"
