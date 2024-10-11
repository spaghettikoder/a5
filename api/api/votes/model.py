from sqlalchemy import Column, Integer
from db import Base


class PostVote(Base):
    __tablename__ = "post_votes"
    
    post_vote_id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    user_id = Column(Integer)