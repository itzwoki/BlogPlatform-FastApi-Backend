from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from sqlalchemy.orm import Session

from pydantic_schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from db.db_setup import get_db
from dependencies.current_user import get_current_user
from commentRoutes.utils import create_comment, get_all_comments, update_comment, del_comment, get_comments, like

router=APIRouter(prefix="/comment")

#Make a cmnt on a Post

@router.post("/{post_id}", response_model=CommentResponse)
async def create_new_comment(
    comment: CommentCreate,
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id
    new_comment = await create_comment(db, comment, post_id, user_id)
    return new_comment

# get all comments on a post

@router.get("/getcomments/{post_id}", response_model=List[CommentResponse])
async def get_comments_on_post(
    post_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized."
        )
    
    all_comments = await get_all_comments(db, post_id, skip, limit)
    return all_comments

# update comment
@router.put("/{comment_id}", response_model=CommentResponse)
async def comment_update(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  
):
    user_id = current_user.id
    comment = await update_comment(db, comment_id, comment_data, user_id)
    return comment

#delete comment
@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id
    await del_comment(db, comment_id, user_id)

    return{
        "message" : "Deleted!."
    }

# get all comments made by a specific user

@router.get("/user-comments", response_model=List[CommentResponse])
async def get_all_user_comments(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id
    comments = await get_comments(db, user_id)
    return comments

# Like a comment

@router.patch("/likes/{comment_id}", response_model=CommentResponse)
async def like_comment(
        comment_id: int,
        db: Session = Depends(get_db),
        current_user : dict =  Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Allowed."
        )
    
    liked_comment =await like(db, comment_id)
    return liked_comment