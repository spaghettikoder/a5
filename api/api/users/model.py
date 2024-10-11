from sqlalchemy import Column, Integer, String
from db import Base


class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
