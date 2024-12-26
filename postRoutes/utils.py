from sqlalchemy.orm import Session

from db.models.post import Post
from pydantic_schemas.post import PostCreate, PostUpdate

from typing import List
from fastapi import HTTPException, status


def create_post(db: Session, post_data: PostCreate, user_id: int):
    new_post = Post(
        title = post_data.title,
        content= post_data.content,
        author_id = user_id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

async def get_posts(db: Session, skip: int = 0, limit: int = 10) -> List[Post]:
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

async def get_post(db:Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {post_id} not found.")
    
    return post

async def update_post(db: Session, post_id: int, post_data: PostUpdate, user_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found."
        )
    if post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized."
        )
    
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content

    db.add(post)
    db.commit()
    db.refresh(post)

    return post

async def delete(db: Session, post_id: int, user_id:int):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found."
        )
    if post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized."
        )
    
    print(post)
    db.delete(post)
    db.commit()
    print("Commit executed")
    

async def get_by_title(db: Session, title: str, skip: int = 0, limit: int =10):
    posts = db.query(Post).filter(Post.title.ilike(f"%{title}%")).offset(skip).limit(limit).all()

    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not Posts Found with the given Title"
        )
    
    return posts