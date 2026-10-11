from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from . import models, database
from .security import hash_pwd, verify_pwd, SECRET, ALGO, create_token
from .schemas import RegisterIn
from datetime import datetime

router = APIRouter(prefix="/api/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = db.query(models.User).filter(models.User.email==email).first()
    if not user: raise HTTPException(401, "User not found")
    return user

@router.post("/register")
def register(req: RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email==req.email).first():
        raise HTTPException(400, "Email exists")
    u = models.User(email=req.email, hashed_password=hash_pwd(req.password), balance=50000)
    db.add(u); db.commit()
    return {"msg": "Registered ma!"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==form.username).first()
    if not user or not verify_pwd(form.password, user.hashed_password):
        raise HTTPException(401, "Wrong credentials")
    token = create_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}