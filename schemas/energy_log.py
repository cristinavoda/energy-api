from pydantic import BaseModel
from datetime import datetime

class EnergyLogCreate(BaseModel):
    energy: int
    timestamp: datetime
    building_id: int


class EnergyLogResponse(BaseModel):
    id: int
    energy: int
    timestamp: datetime
    building_id: int

    class Config:
        from_attributes = True