# app/api/routes/auth.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.api.deps import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginSchema, RegisterSchema
from app.schemas.auth import LoginResponse, RegisterResponse



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.

    - **data**: Dados de registro contendo nome, email e senha.
    - **db**: Sessão do banco de dados.

    Retorna uma mensagem de sucesso e o ID do usuário criado.
    """
    service = AuthService(db)
    return service.register(data)

@router.post("/login", response_model=LoginResponse)
def login(data: LoginSchema, db: Session = Depends(get_db)):
    """
    Autentica o usuário com email e senha.

    - **data**: Dados de login contendo email e senha.
    - **db**: Sessão do banco de dados.

    Retorna um token de acesso se as credenciais forem válidas.
    """
    service = AuthService(db)
    return service.login(data.email, data.password)
