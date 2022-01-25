from pydantic import ColorError
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
     __tablename__="posts"
     id = Column(Integer,primary_key=True)
     posts=Column(String,nullable=False)
     title=Column(String,nullable=False)
     published=Column(name='published',type_=Boolean,server_default="true",nullable=False)
