from pydantic import BaseModel

class BuildingCreate(BaseModel):
    name: str
    lat: float
    lng: float
    energy: int


class BuildingOut(BuildingCreate):
    id: int

    class Config:
        from_attributes = True