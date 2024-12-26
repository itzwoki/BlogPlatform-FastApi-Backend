from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from pydantic_schemas.post import PostCreate, PostResponse, PostUpdate
from db.db_setup import get_db
from postRoutes.utils import create_post, get_posts, get_post, update_post, delete, get_by_title
from dependencies.current_user import get_current_user

router=APIRouter(prefix="/post")

## create a post
@router.post("/create-post", response_model=PostResponse)
def add_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    user_id = current_user.id
    return create_post(db, post, user_id)

## get all posts from the DB
@router.get("/")
async def get_all_posts(
    db: Session = Depends(get_db),
    skip: int=0,
    limit: int=10,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized."
        )
    posts = await get_posts(db, skip, limit)
    return posts

# get a specific post by ID

@router.get("/{post_id}", response_model=PostResponse)
async def get_post_by_id(
        post_id: int,
        db: Session = Depends(get_db),
        current_user : dict = Depends(get_current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Un-Authorized"
        )
    post = await get_post(db, post_id)
    return post

    #get by title

@router.get("/title/search")
async def get_post_by_title(
    title: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    posts = await get_by_title(db, title, skip, limit)
    return posts


# Update a Post Fully or partially

@router.put("/update/{post_id}", response_model=PostResponse)
async def post_update(
    post_id : int,
    post_data : PostUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.id
    post = await update_post(db, post_id, post_data, user_id)
    return post

# delete a post (ID)

@router.delete("/delete/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user : dict = Depends(get_current_user)
):
    user_id = current_user.id
    await delete(db, post_id, user_id)

    return{
        "message" : f"Post with ID:{post_id} deleted."
    }