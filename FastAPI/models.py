from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.ext.declarative import declarative_base

# データベース作成
Base = declarative_base()

# violatorテーブル作成
class Violator(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    cam_no = Column(Integer)
    date = Column(String)
    violation = Column(String)
    image = Column(BLOB)
