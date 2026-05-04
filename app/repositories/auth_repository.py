# app/repositories/auth_repository.py

from app.models.user import Users


class AuthRepository:
    def __init__(self, db):
        self.db = db

    def get_by_email(self, email: str):
        return self.db.query(Users).filter(Users.email == email).first()

    def create_user(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
