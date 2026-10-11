from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = os.getenv("SECRET_KEY", "supersecretjwtkey123456789")
ALGO = "HS256"

security = HTTPBearer() # NEW - for dashboard auth

def hash_pwd(p): return pwd_context.hash(p)
def verify_pwd(p, h): return pwd_context.verify(p, h)

def create_token(data: dict):
    exp = datetime.utcnow() + timedelta(hours=2)
    data.update({"exp": exp})
    return jwt.encode(data, SECRET, algorithm=ALGO)

def luhn_check(num: str) -> bool:
    s=0; rev=num[::-1]
    for i,d in enumerate(rev):
        n=int(d)
        if i%2==1: n*=2; n=n-9 if n>9 else n
        s+=n
    return s%10==0

# NEW - Dashboard ku JWT check panna idhu use aagum
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        user_id = payload.get("sub") # login panna token la sub: user.id nu irukanum
        if user_id is None:
            raise HTTPException(status_code=401, detail="JWT authentication failed")
        return int(user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="JWT authentication failed. Please login again.")