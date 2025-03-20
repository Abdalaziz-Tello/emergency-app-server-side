from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import User
from auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(username: str, password: str, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_pw = hash_password(password)
    user = User(username=username, password=hashed_pw)
    session.add(user)
    session.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user.username}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
