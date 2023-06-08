#!/usr/bin/env python3
""" User Module """
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """Represents a user in the database."""

    __tablename__: str = 'users'

    id: Column = Column(Integer, primary_key=True)
    email: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)
    session_id: Column = Column(String, nullable=True)
    reset_token: Column = Column(String, nullable=True)
