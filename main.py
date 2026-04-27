from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models.building import Building
from models.energy_log import EnergyLog
from schemas.energy_log import EnergyLogCreate
from schemas.building import BuildingCreate, BuildingOut

import random
from datetime import datetime, timedelta
@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_data()
    seed_logs()
    yield
app = FastAPI(lifespan=lifespan)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_data():
    db = SessionLocal()

    if db.query(Building).count() == 0:
        db.add_all([
            Building(name="Hospital Lleida", lat=41.615, lng=0.63, energy=1200),
            Building(name="School Lleida", lat=41.62, lng=0.61, energy=800),
            Building(name="Library Lleida", lat=41.618, lng=0.625, energy=500),
            Building(name="University Campus", lat=41.61, lng=0.62, energy=1500),
            Building(name="City Hall", lat=41.617, lng=0.621, energy=900),
            Building(name="Sports Center", lat= 41.619, lng= 0.635, energy=700),

        ])
        db.commit()

    db.close()

def seed_logs():
    db = SessionLocal()
    try:
        if db.query(EnergyLog).count() == 0:
            buildings = db.query(Building).all()

            logs = []
            for b in buildings:
                for i in range(10):
                    logs.append(
                        EnergyLog(
                            energy=random.randint(400, 1500),
                            timestamp=datetime.utcnow() - timedelta(hours=i, minutes=random.randint(0, 59)),
                            building_id=b.id
                        )
                    )

            db.bulk_save_objects(logs)  
            db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200","https://energy-dashboard-app.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")



buildings = [
    {"name": "Hospital Lleida", "lat": 41.615, "lng": 0.63, "energy": 1200},
    {"name": "School Lleida", "lat": 41.62, "lng": 0.61, "energy": 800},
    {"name": "Library Lleida", "lat": 41.618, "lng": 0.625, "energy": 500},
  {"name": "University Campus", "lat": 41.61, "lng": 0.62, "energy": 1500},
  {"name": "City Hall", "lat": 41.617, "lng": 0.621, "energy": 900},
  {"name": "Sports Center", "lat": 41.619, "lng": 0.635, "energy": 700},
  {"name": "Public Offices", "lat": 41.613, "lng": 0.628, "energy": 1100},
  {"name": "Cultural Center", "lat": 41.616, "lng": 0.64, "energy": 650},
  {"name": "Fire Station", "lat": 41.622, "lng": 0.627, "energy": 950},
  {"name": "Police Station", "lat": 41.623, "lng": 0.615, "energy": 1000},
  {"name": "Primary School A", "lat": 41.614, "lng": 0.61, "energy": 600},
  {"name": "Primary School B", "lat": 41.626, "lng": 0.63, "energy": 750},
  {"name": "Health Center", "lat": 41.612, "lng": 0.618, "energy": 850},
  {"name": "Library North", "lat": 41.627, "lng": 0.622, "energy": 550},
  {"name": "Transport Hub", "lat": 41.609, "lng": 0.635, "energy": 1300}
]

@app.get("/")
def root():
    return {"message": "Energy API running 🚀"}

@app.get("/buildings")
def get_buildings(db: Session = Depends(get_db)):
    try:
        return db.query(Building).all()
    finally:
        db.close()

@app.get("/buildings/{id}")
def get_building(id: int, db: Session = Depends(get_db)):
    try:
        return db.get(Building, id)
    finally:
        db.close()

@app.post("/buildings")
def create_building(b: BuildingCreate, db: Session = Depends(get_db)):
    try:
        new = Building(
            name=b.name,
            lat=b.lat,
            lng=b.lng,
            energy=b.energy
        )
        db.add(new)
        db.commit()
        db.refresh(new)
        return new
    finally:
        db.close()

@app.put("/buildings/{id}")
def update_building(id: int, b: BuildingCreate, db: Session = Depends(get_db)):
    try:
        building = db.get(Building, id)

        building.name = b.name
        building.energy = b.energy

        db.commit()
        db.refresh(building)

        return building
    finally:
        db.close()

@app.delete("/buildings/{id}")
def delete_building(id: int, db: Session = Depends(get_db)):
    try:
        building = db.get(Building, id)

        db.delete(building)
        db.commit()

        return {"ok": True}
    finally:
        db.close()

@app.post("/energy")
def create_log(log: EnergyLogCreate, db: Session = Depends(get_db)):
    try:
        new_log = EnergyLog(**log.dict())

        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        return new_log
    finally:
        db.close()

@app.get("/buildings/{id}/energy")
def get_energy_logs(id: int, db: Session = Depends(get_db)):
    try:
        return db.query(EnergyLog).filter(EnergyLog.building_id == id).all()
    finally:
        db.close()


