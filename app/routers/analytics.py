from fastapi import APIRouter, Depends, Query
from typing import List, Optional, Any
from sqlalchemy import func  # type: ignore[reportMissingImports]
from math import radians, cos, sin, asin, sqrt

from .. import models
from ..database import get_sessionmaker

router = APIRouter(prefix="/analytics", tags=["analytics"])


def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/count")
def total_count(db: Any = Depends(get_db)):
    return {"count": db.query(models.EVStation).count()}


@router.get("/count_by_country")
def count_by_country(limit: int = 50, db: Any = Depends(get_db)):
    func_count = func.count(models.EVStation.id)
    q = db.query(models.EVStation.country, func_count).group_by(models.EVStation.country).order_by(func_count.desc()).limit(limit)
    return [{"country": row[0], "count": row[1]} for row in q]


def haversine(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


@router.get("/nearest")
def nearest_stations(lat: float = Query(...), lon: float = Query(...), radius_km: float = 10.0, limit: int = 10, db: Any = Depends(get_db)):
    # naive in-Python filter (works fine for small datasets)
    stations = db.query(models.EVStation).filter(models.EVStation.lat.isnot(None), models.EVStation.lon.isnot(None)).all()
    nearby = []
    for s in stations:
        dist = haversine(lat, lon, s.lat, s.lon)
        if dist <= radius_km:
            nearby.append((dist, s))
    nearby.sort(key=lambda x: x[0])
    return [{"distance_km": d, "station": {
        "id": s.id, "title": s.title, "lat": s.lat, "lon": s.lon, "town": s.town, "country": s.country
    }} for d, s in nearby[:limit]]


@router.get("/by_operator")
def by_operator(operator: str, db: Any = Depends(get_db)):
    return db.query(models.EVStation).filter(models.EVStation.operator == operator).all()
