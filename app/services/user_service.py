# app/services/user_service.py

from fastapi import HTTPException
from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db):
        self.repo = UserRepository(db)

    # Apenas o admin pode listar todos os usuários
    def list_users(self, current_user, skip, limit):
        if current_user.role != "admin":
            raise HTTPException(403, "Not allowed")

        return self.repo.get_all(skip, limit)

    # O usuário pode ver seus próprios dados, ou o admin
    def get_user(self, user_id, current_user):
        user = self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(404, "User not found")

        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(403, "Not allowed")

        return user

    # O usuário pode atualizar seus próprios dados, ou o admin
    def update_user(self, user_id, data, current_user):
        user = self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(404, "User not found")

        # permissão
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(403, "Not allowed")

        # email duplicado
        if data.email:
            existing = self.repo.get_by_email(data.email)
            if existing and existing.id != user_id:
                raise HTTPException(400, "Email already registered")
            user.email = data.email

        if data.name:
            user.name = data.name

        if data.password:
            user.hashed_password = generate_password_hash(data.password)

        if data.role:
            if current_user.role != "admin":
                raise HTTPException(403, "Not allowed to change role")

            if data.role not in ["admin", "user"]:
                raise HTTPException(400, "Invalid role")

            user.role = data.role

        return self.repo.update(user)

    # O usuário pode deletar sua própria conta, ou o admin  
    def delete_user(self, user_id, current_user):
        user = self.repo.get_by_id(user_id)

        if not user:
            raise HTTPException(404, "User not found")

        # permissão
        if current_user.role != "admin" and current_user.id != user_id:
            raise HTTPException(403, "Not allowed")

        self.repo.delete(user)
        return user

