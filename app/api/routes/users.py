# app/api/users.py

from db.base import Base
from api.deps import get_db
from models.user import Users
from core.config import Config
from core.dependencies import get_current_user
from schemas.user import UserResponse, UserUpdate

from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from werkzeug.security import generate_password_hash
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
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
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
    existing = db.query(Users).filter(Users.email == data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if existing and existing.id != user_id:
        raise HTTPException(status_code=400, detail="Email already registered")

    # permissão
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    if data.name is not None:
        user.name = data.name
    if data.email is not None:
        user.email = data.email
    if data.password is not None:
        user.hashed_password = generate_password_hash(data.password)
    if data.role and current_user.role != "admin":
        raise HTTPException(403, "Not allowed to change role")
    elif data.role:
        role = ["admin", "user"]
        if data.role not in role:
            raise HTTPException(status_code=400, detail="Invalid role")
        user.role = data.role

    db.commit()
    db.refresh(user)

    return user

# Deletar usuário
@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session=Depends(get_db), current_user: Users = Depends(get_current_user)):
    """ 
    Deleta um usuário.
    Apenas administradores ou o próprio usuário podem deletar.
    - **user_id**: ID do usuário a ser deletado.
    - **db**: Sessão do banco de dados.
    - **current_user**: Usuário autenticado.
    Retorna os dados do usuário deletado.
    """
    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Permissão
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    
    # Deletar Usuário
    db.delete(user)
    db.commit()

    # return user
    return JSONResponse(content={"message": "User deleted successfully", "user_id": user_id}, status_code=200)

