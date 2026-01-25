from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from schemas.user import UserResponse, UserCreate, UserLogin

from db.database import SessionLocal
from db.models.user import User


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashpassword(pwd):
    print(f"Got password: {pwd}")
    return pwd_context.hash(pwd)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/signup", response_model=UserResponse)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        return HTTPException(status_code=400, detail={'error': 'User already exists'})

    hashed_password = hashpassword(payload.password)
    user = User(full_name=payload.full_name, email=payload.email, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.post("/login", response_model=UserResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    password = payload.password
    email = payload.email
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user:
        return HTTPException(status_code=404, detail={'error': 'User not found'})

    if not verify_password(password, db_user.hashed_password):
        return HTTPException(status_code=400, detail={'error': 'Invalid credentials'})
    
    return db_user
