from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# よくわかんないけど必要
class ViolatorBase(BaseModel):
    cam_no: int
    date: str
    violation: str
    image: bytes
    last_modified: datetime
    tracking_id: str

class ViolatorCreate(ViolatorBase):
    pass

class Violator(ViolatorBase):
    id: int

    class Config:
        orm_mode = True
