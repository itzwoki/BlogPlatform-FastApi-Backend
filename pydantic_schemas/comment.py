from pydantic import BaseModel

from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    content: str 

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(CommentCreate):
    id: int
    author_id : int
    likes: int
    created_at: datetime
    updated_at: datetime

    class Config():
        orm_mode = True