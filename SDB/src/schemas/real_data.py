import pydantic
from datetime import datetime

class LineData(pydantic.BaseModel):
    timestamp: str
    Line_length: int

class InCafeteriaData(pydantic.BaseModel):
    timestamp: str
    num_in_cafeteria: int

class AllData(pydantic.BaseModel):
    timestamp: str
    Line_length: int
    num_in_cafeteria: int

    def set_Line_length(self, Line_length):
        self.Line_length = Line_length

    def set_num_in_cafeteria(self, num_in_cafeteria):
        self.num_in_cafeteria = num_in_cafeteria

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

class PredictData(pydantic.BaseModel):
    data: list
    starttime: datetime
