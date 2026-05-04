# app/api/routes/auth.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from api.deps import get_db
from services.auth_service import AuthService
from schemas.auth import LoginSchema, RegisterSchema



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.

    - **data**: Dados de registro contendo nome, email e senha.
    - **db**: Sessão do banco de dados.

    Retorna uma mensagem de sucesso e o ID do usuário criado.
    """
    service = AuthService(db)
    return service.register(data)

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    """
    Autentica o usuário com email e senha.

    - **data**: Dados de login contendo email e senha.
    - **db**: Sessão do banco de dados.

    Retorna um token de acesso se as credenciais forem válidas.
    """
    service = AuthService(db)
    return service.login(data.email, data.password)
