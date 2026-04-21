from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import engine
from models import Base
from database import SessionLocal
from models import Building
from schemas import BuildingCreate
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://energy-dashboard-app.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def get_buildings():
    db = SessionLocal()
    try:
        return db.query(Building).all()
    finally:
        db.close()

@app.get("/buildings/{id}")
def get_building(id: int):
    db = SessionLocal()
    try:
        return db.get(Building, id)
    finally:
        db.close()        

@app.post("/buildings")
def create_building(b: BuildingCreate):
    db = SessionLocal()
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
def update_building(id: int, b: dict):
    db = SessionLocal()
    try:
        building = db.get(Building, id)

        building.name = b["name"]
        building.energy = b["energy"]

        db.commit()
        db.refresh(building)

        return building
    finally:
        db.close()

@app.delete("/buildings/{id}")
def delete_building(id: int):
    db = SessionLocal()
    try:
        building = db.get(Building, id)

        db.delete(building)
        db.commit()

        return {"ok": True}
    finally:
        db.close()