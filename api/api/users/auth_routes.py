from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import model
import auth
import user_schemas

from db import get_db


SESSION = 0


router = APIRouter(
    prefix="/user",
    tags=["User Authentication"],
    dependencies=[Depends(get_db)]
)


@router.post(
    "/register",
    response_model=user_schemas.UserInDB,
    status_code=200,
    summary="""The endpoint `/register` registers a new user by storing their username, password in PostgreSQL database.""",
)
async def register(
    user: user_schemas.User,
    db: Session = router.dependencies[SESSION],
):
    db_user: user_schemas.UserInDB = await auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = model.User(username=user.username)

    db.add(db_user)
    db.commit()

    return db_user

@router.get(
    "/check_user/{user_id}",
    response_model=user_schemas.UserInDB,
    status_code=200,
    summary="""The endpoint `/check_user` checks if a given user exists by user_id in the database.""",
)
async def check_user(
    user_id: int,
    db: Session = router.dependencies[SESSION],
):
    db_user = await auth.get_user_by_id(db, user_id=user_id)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_user

