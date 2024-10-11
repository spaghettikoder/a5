from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserInDB(BaseModel):
    user_id: int
    username: str
