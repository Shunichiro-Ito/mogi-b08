from .Base import Base
from sqlalchemy import Column, Integer, DateTime

class InCafeteriaDataModel(Base):
    __tablename__ = "incafe_data"
    timestamp = Column(DateTime, primary_key=True, index=True, nullable=False)
    num_in_cafeteria = Column(Integer, nullable=False)