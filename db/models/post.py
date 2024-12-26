from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db_setup import Base
from .mixins import TimeStamp

class Post(TimeStamp, Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)


    #relationship with users and comment tables
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="posts", cascade="all, delete-orphan")
