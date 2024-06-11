from enum import Enum
from pydantic import BaseModel, Field

class CafeteriaStatus(Enum):
    LOW = "LOW"
    MIDIUM = "MIDIUM"
    HIGH = "HIGH"
    CLOSED = "CLOSED"

    @classmethod
    def from_int(cls, n: int):
        if n == 0:
            return cls.LOW
        elif n == 1:
            return cls.MIDIUM
        elif n == 2:
            return cls.HIGH
        elif n == 3:
            return cls.CLOSED
        else:
            raise ValueError("Invalid value")


class CafeteriaStatusResponse(BaseModel):
    status: CafeteriaStatus = Field(..., example="LOW")