from sqlalchemy import Column, Integer, String, Text
from db import Base


class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    votes_count = Column(Integer, default=0)
