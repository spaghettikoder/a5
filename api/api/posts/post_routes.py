from db import get_db
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import requests
import model
import post_schemas
import post_utils

router = APIRouter(
    prefix="/post",
    tags=["Post Maintenance"],
    dependencies=[Depends(get_db)]
)

@router.post("/create", response_model=post_schemas.PostInDB, status_code=201)
def create_post(post: post_schemas.CreatePost, db: Session = Depends(get_db)):
    url = f'http://localhost:8000/user/check_user/{post.user_id}'
    response = requests.get(url)

    if response.status_code == 404:
        raise HTTPException(status_code=400, detail="User does not exist")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to validate user existence")

    new_post = model.Post(
        user_id=post.user_id,
        title=post.title,
        content=post.content
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get(
    "/check_post/{post_id}",
    response_model=post_schemas.PostInDB,
    status_code=200,
    summary="Check if a post exists by post_id"
)
async def check_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    db_post:post_schemas.PostInDB = await post_utils.get_post_by_id(db, post_id=post_id)

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/feed", response_model=post_schemas.AvailablePosts, status_code=200)
async def get_feed(db: Session = Depends(get_db)):
    posts = db.query(model.Post).limit(10).all()
    return {"posts": posts}