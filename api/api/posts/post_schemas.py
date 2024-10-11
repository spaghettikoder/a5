from pydantic import BaseModel
from typing import List
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str

class CreatePost(BaseModel):
    title: str
    content: str
    username: str
    user_id: int

class PostInDB(Post):
    post_id: int
    user_id: int
    votes_count: int


class PostUID(BaseModel):
    post_id: int


class AvailablePosts(BaseModel):
    posts: List[PostInDB]
