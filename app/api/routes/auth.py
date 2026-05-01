
from app.db.base import Base
from app.api.deps import get_db
from app.models.user import Users
from app.core.config import Config
from werkzeug.security import generate_password_hash
from app.schemas.auth import LoginSchema, RegisterSchema
from app.core.security import authenticate_user, create_access_token

from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends



router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token(user.id)
    return {"access_token": token}


@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = generate_password_hash(data.hashed_password)
    new_user = Users(name=data.name, email=data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}
