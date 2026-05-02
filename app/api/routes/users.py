# app/api/users.py

from app.db.base import Base
from app.api.deps import get_db
from app.models.user import Users
from app.core.config import Config
from app.core.dependencies import get_current_user
from app.schemas.user import UserResponse, UserUpdate

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends



router = APIRouter(prefix="/users", tags=["users"])

# Listar usuários
@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    """
    Lista todos os usuários.

    Requer permissões de administrador.

    - **db**: Sessão do banco de dados.
    - **current_user**: Usuário autenticado.

    Retorna uma lista de usuários.
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    return db.query(Users).all()

# Buscar usuário por ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session=Depends(get_db), current_user: Users = Depends(get_current_user)):
    """
    Busca um usuário pelo ID.

    Apenas administradores ou o próprio usuário podem acessar.

    - **user_id**: ID do usuário a ser buscado.
    - **db**: Sessão do banco de dados.
    - **current_user**: Usuário autenticado.

    Retorna os dados do usuário.
    """
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # só admin ou o próprio usuário pode ver
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return user

# Atualizar usuário
@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    """
    Atualiza os dados de um usuário.

    Apenas administradores ou o próprio usuário podem atualizar.

    - **user_id**: ID do usuário a ser atualizado.
    - **data**: Dados a serem atualizados (ex.: nome).
    - **db**: Sessão do banco de dados.
    - **current_user**: Usuário autenticado.

    Retorna os dados atualizados do usuário.
    """
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # permissão
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if data.name is not None:
        user.name = data.name

    db.commit()
    db.refresh(user)

    return user

# Deletar usuário
# Upgrade importante (admin only)

