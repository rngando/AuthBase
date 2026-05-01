# app/core/security.py

from app.models.user import Users
from app.core.config import Config
from datetime import datetime, timedelta

import jwt
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash



def authenticate_user(db: Session, email: str, password: str):
    # Verificar se o Usuário existe para autenticar ele
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return None
    if not check_password_hash(user.hashed_password, password):
        return None
    return user

def create_access_token(user_id: int):
    # Criar o TOKEN de acesso para cada Usuário
    expiration = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expiration
    }

    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token

