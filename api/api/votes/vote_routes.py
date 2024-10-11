from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import requests
import model
import vote_schemas
from db import get_db

router = APIRouter(
    prefix="/vote",
    tags=["Vote Maintenance"]
)

@router.post(
    "/vote_for_post",
    response_model=vote_schemas.PostVoteInDB,
    status_code=200,
    summary="""The endpoint `/vote_for_post` allows any user to vote for a post.""",
)
def vote_for_post(
    vote: vote_schemas.PostVote,
    db: Session = Depends(get_db),
):
    url_user = f'http://localhost:8000/user/check_user/{vote.user_id}'
    response_user = requests.get(url_user)

    if response_user.status_code == 404:
        raise HTTPException(status_code=400, detail="User does not exist") 
    if response_user.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to validate user existence")

    url_post = f'http://localhost:8001/post/check_post/{vote.post_id}'
    response_post = requests.get(url_post)

    if response_post.status_code == 404:
        raise HTTPException(status_code=400, detail="Post does not exist")
    if response_post.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to validate post existence")

    db_vote = db.query(model.PostVote).filter(
        model.PostVote.user_id == vote.user_id,
        model.PostVote.post_id == vote.post_id
    ).first()

    if db_vote:
        raise HTTPException(status_code=400, detail="User has already voted for this post")

    new_vote = model.PostVote(
        post_id=vote.post_id,
        user_id=vote.user_id
    )
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return new_vote
