from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class EVStationBase(BaseModel):
    title: Optional[str] = None
    address: Optional[str] = None
    town: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    operator: Optional[str] = None
    status: Optional[str] = None
    num_connectors: Optional[int] = None
    connector_types: Optional[str] = None
    date_added: Optional[datetime] = None


class EVStationCreate(EVStationBase):
    id: Optional[int] = None


class EVStationUpdate(EVStationBase):
    pass


class EVStationOut(EVStationBase):
    id: int

    class Config:
        orm_mode = True
