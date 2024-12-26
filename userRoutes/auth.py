from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db.db_setup import get_db
from db.models.user import User
from pydantic_schemas.user import UserCreate, UserLogin
from .utils.loginutil import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=400, detail="Username Already Exist.")
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email Already Exist.")
    
    hashed_password = hash_password(user.password)
    new_user = User(username= user.username, email = user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{
        "message" : "User Registered",
        "user" : {
            "id" : new_user.id,
            "username" : new_user.username,
            "email" : new_user.email,
        }
    }

@router.post("/login")
async def login(user:UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Username Doesn't Exist.")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Password.")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}