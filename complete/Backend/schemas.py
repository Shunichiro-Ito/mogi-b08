from pydantic import BaseModel
from typing import Optional

# よくわかんないけど必要
class ViolatorBase(BaseModel):
    cam_no: int
    date: str
    violation: str
    image: bytes

class ViolatorCreate(ViolatorBase):
    pass

class Violator(ViolatorBase):
    id: int

    class Config:
        orm_mode = True
