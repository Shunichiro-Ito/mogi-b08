from sqlalchemy import Column, Integer, DateTime
from .Base import Base

class LineDataModel(Base):
    __tablename__ = "line_data"
    timestamp = Column(DateTime, primary_key=True, index=True, nullable=False)
    Line_length = Column(Integer, nullable=False)