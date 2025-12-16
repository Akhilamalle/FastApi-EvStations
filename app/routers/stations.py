from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_sessionmaker, get_engine

router = APIRouter(prefix="/stations", tags=["stations"])


def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.EVStationOut])
def read_stations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.EVStation).offset(skip).limit(limit).all()


@router.get("/{station_id}", response_model=schemas.EVStationOut)
def read_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(models.EVStation).get(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@router.post("/", response_model=schemas.EVStationOut, status_code=status.HTTP_201_CREATED)
def create_station(payload: schemas.EVStationCreate, db: Session = Depends(get_db)):
    station = models.EVStation(**payload.dict(exclude_unset=True))
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


@router.put("/{station_id}", response_model=schemas.EVStationOut)
def update_station(station_id: int, payload: schemas.EVStationUpdate, db: Session = Depends(get_db)):
    station = db.query(models.EVStation).get(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(station, k, v)
    db.add(station)
    db.commit()
    db.refresh(station)
    return station


@router.delete("/{station_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_station(station_id: int, db: Session = Depends(get_db)):
    station = db.query(models.EVStation).get(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    db.delete(station)
    db.commit()
    return None
