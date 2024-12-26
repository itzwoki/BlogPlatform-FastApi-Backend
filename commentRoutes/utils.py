from sqlalchemy.orm import Session

from db.models.comment import Comment
from pydantic_schemas.comment import CommentCreate,CommentUpdate

from fastapi import HTTPException, status
from typing import List

async def create_comment(db: Session, post_comment: CommentCreate,post_id:int,  user_id: int):
    new_comment=Comment(
        content= post_comment.content,
        post_id=post_id,
        author_id= user_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

async def get_all_comments(db: Session, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
    comments = db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
    return comments

async def update_comment(db: Session, comment_id: int, comment_data: CommentUpdate, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not Found"
        )
    if comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized."
        )
    
    if comment_data.content is not None:
        comment.content = comment_data.content

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment