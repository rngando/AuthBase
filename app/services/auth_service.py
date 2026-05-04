# app/services/user_service.py

from fastapi import HTTPException
from werkzeug.security import generate_password_hash

from app.models.user import Users
from app.repositories.auth_repository import AuthRepository
from app.core.security import authenticate_user, create_access_token


class AuthService:
    def __init__(self, db):
        self.repo = AuthRepository(db)

    def login(self, email: str, password: str):
        user = authenticate_user(self.repo.db, email, password)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        token = create_access_token(user.id)
        return {"access_token": token, "token_type": "bearer"}

    def register(self, data):
        existing_user = self.repo.get_by_email(data.email)

        if existing_user:
            raise HTTPException(400, "Email already registered")

        hashed_password = generate_password_hash(data.password)

        new_user = Users(
            name=data.name,
            email=data.email,
            hashed_password=hashed_password
        )

        user = self.repo.create_user(new_user)

        return {
            "message": "User registered successfully",
            "user_id": user.id
        }

