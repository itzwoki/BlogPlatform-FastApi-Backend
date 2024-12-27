from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy import func
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db.db_setup import get_db
from db.models.user import User
from db.models.post import Post
from db.models.comment import Comment
from pydantic_schemas.user import UserCreate, UserLogin, userDetails
from .utils.loginutil import verify_password, create_access_token
from dependencies.current_user import get_current_user


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


@router.get("/user-details", response_model=userDetails)
async def get_user_details(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized."
        )
    
    posts_count = (
        db.query(func.count(Post.id))
        .filter(Post.author_id == user_id)
        .scalar()
    )

    total_likes = (
        db.query(func.count(Comment.likes))
        .filter(Comment.author_id == user_id)
        .scalar() or 0
    )

    return {
        "username" : user.username,
        "email" : user.email,
        "posts_count" : posts_count,
        "total_likes" : total_likes
    }
