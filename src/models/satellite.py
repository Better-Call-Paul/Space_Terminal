# app/models/satellite.py
from sqlalchemy import Column, Integer, Float, Boolean

class Satellite(Base):
    __tablename__ = "satellites"
    
    id = Column(Integer, primary_key=True, index=True)
    sat_id = Column(Integer, unique=True, index=True, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    altitude = Column(Integer)
    azimuth = Column(Float)
    elevation = Column(Float)
    ra = Column(Float)
    dec = Column(Float)
    timestamp = Column(Integer)
    eclipsed = Column(Boolean)
