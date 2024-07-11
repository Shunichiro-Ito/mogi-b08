from pydantic import BaseModel
from datetime import datetime

# よくわかんないけど必要
class ViolatorBase(BaseModel):
    cam_no: str
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
