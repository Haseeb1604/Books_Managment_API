from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .Database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    usertype = Column(
        String, nullable=False, server_default='normal')
    created_At = Column(
        TIMESTAMP(timezone=True), nullable=False, 
        server_default=text('now()')
        )

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    created_At = Column(
        TIMESTAMP(timezone=True), nullable=False, 
        server_default=text('now()')
        )

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    auther_id = Column(Integer, ForeignKey("auther.id", ondelete="CASCADE"), nullable=False)
    publisher_id = Column(Integer, ForeignKey("publisher.id", ondelete="CASCADE"),  nullable=False)

    owner = relationship("Users")
    auther = relationship("Auther")
    publisher = relationship("Publisher")

class Auther(Base):
    __tablename__ = "auther"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_At = Column(
        TIMESTAMP(timezone=True), nullable=False, 
        server_default=text('now()')
        )

class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_At = Column(
        TIMESTAMP(timezone=True), nullable=False, 
        server_default=text('now()')
        )