from pydantic import BaseModel, EmailStr

from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password : str

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username : str 
    email : EmailStr
    created_at : datetime

class userDetails(BaseModel):
    username: str
    email:  EmailStr
    posts_count: int
    total_likes: int
    
    class Config():
        orm_mode = True 