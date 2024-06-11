# In this file, we define the User model, which is used to store user data in the database.
from sqlalchemy import Column, Integer, String
from .Base import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)