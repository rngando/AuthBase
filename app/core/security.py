# app/core/security.py

from app.models.user import Users
from app.core.config import Config
from app.repositories.user_repository import UserRepository

import jwt
from sqlalchemy.orm import Session
from datetime import datetime, UTC, timedelta
from werkzeug.security import generate_password_hash, check_password_hash



def authenticate_user(db: Session, email: str, password: str):
    # Verificar se o Usuário existe para autenticar ele
    service = UserRepository(db)
    
    user = service.get_by_email(email)
    if not user:
        return None
    if not check_password_hash(user.hashed_password, password):
        return None
    return user

def create_access_token(user_id: int):
    # Criar o TOKEN de acesso para cada Usuário
    expiration = datetime.now(UTC) + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user_id),
        "exp": expiration
    }

    token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return token

