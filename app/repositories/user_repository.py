# repositories/user_repository.py

from models.user import Users

class UserRepository:
    def __init__(self, db):
        self.db = db

    # Pegar todos os usuários, com paginação
    def get_all(self, skip=0, limit=10):
        return self.db.query(Users).offset(skip).limit(limit).all()

    # pegar usuário por id
    def get_by_id(self, user_id: int):
        return self.db.query(Users).filter(Users.id == user_id).first()

    # Pegar usuário por email
    def get_by_email(self, email: str):
        return self.db.query(Users).filter(Users.email == email).first()

    # Criar usuário
    def create(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    # Atualizar usuário
    def update(self, user):
        self.db.commit()
        self.db.refresh(user)
        return user

    # Deletar usuário
    def delete(self, user):
        self.db.delete(user)
        self.db.commit()

