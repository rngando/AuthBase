# app/api/users.py

from app.api.deps import get_db
from app.models.user import Users
from app.services.user_service import UserService
from app.core.dependencies import get_current_user
from app.schemas.user import UserResponse, UserUpdate

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends



router = APIRouter(prefix="/users", tags=["users"])

# Só o admin pode listar todos os usuários
@router.get("/", response_model=list[UserResponse])
def get_users(skip: int=0, limit: int=10, db: Session = Depends(get_db), current_user: Users = Depends(get_current_user)):
    """
    Lista todos os usuários.

    Requer permissões de administrador.

    - **db**: Sessão do banco de dados.
    - **current_user**: Usuário autenticado.

    Retorna uma lista de usuários.
    """
    service = UserService(db)
    return service.list_users(current_user, skip, limit)

@router.get("/me", response_model=UserResponse)
def get_me(db: Session=Depends(get_db), current_user: Users = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.

    - **current_user**: Usuário autenticado.

    Retorna os dados do usuário.
    """
    service = UserService(db)
    return service.get_user(current_user.id, current_user)

# Apenas o admin ou o próprio usuário
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
    service = UserService(db)
    return service.get_user(user_id, current_user)

# Apenas o admin ou o próprio usuário pode atualizar
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
    service = UserService(db)
    return service.update_user(user_id, data, current_user)

# Apenas o admin ou o próprio usuário pode deletar
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
    service = UserService(db)
    return service.delete_user(user_id, current_user)
