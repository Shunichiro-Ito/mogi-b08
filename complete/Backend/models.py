from sqlalchemy import Column, Integer, String, BLOB,DateTime
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

# データベース作成
Base = declarative_base()

# violatorテーブル作成
class Violator(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    cam_no = Column(String)
    date = Column(DateTime(timezone=True))
    violation = Column(String)
    image = Column(BLOB)
    last_modified = Column(DateTime(timezone=True), onupdate=func.now())  # タイムスタンプ
    tracking_id = Column(String)  # トラッキングid

#条件指定
# cam_noが1か2(検索ボックスは1か2)->チェックボックスで1か2選べるようにする
# dataが   開始と終了それぞれを指定(これも)プルダウン
#violation->チェックボックス
