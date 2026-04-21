from pydantic import BaseModel

class BuildingCreate(BaseModel):
    name: str
    lat: float
    lng: float
    energy: int