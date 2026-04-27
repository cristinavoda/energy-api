from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime
from database import Base


class EnergyLog(Base):
    __tablename__ = "energy_logs"

    id = Column(Integer, primary_key=True, index=True)
    energy = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow,nullable=False)

    building_id = Column(Integer, ForeignKey("buildings.id"))