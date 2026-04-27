from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import EnergyLog
from schemas import EnergyLogCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/energy")
def create_energy(log: EnergyLogCreate, db: Session = Depends(get_db)):
    new_log = EnergyLog(**log.dict())
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return new_log