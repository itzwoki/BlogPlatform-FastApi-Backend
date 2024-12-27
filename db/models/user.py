from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import TimeStamp

class User(TimeStamp, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    #Relationship with Post and Comment tables
    posts = relationship("Post", back_populates="author")
    comments =  relationship("Comment", back_populates="author") 