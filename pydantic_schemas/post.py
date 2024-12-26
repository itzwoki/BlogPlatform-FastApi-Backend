from pydantic import BaseModel

from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    title : str
    content: str

class PostUpdate(BaseModel): 
    title: Optional[str] = None
    content: Optional[str] = None

class PostResponse(PostCreate):
    id: int
    author_id : int
    created_at: datetime
    updated_at : datetime

    class Config():
        orm_mode = True