from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EVStation(Base):
    __tablename__ = 'ev_stations'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    address = Column(String, nullable=True)
    town = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    country = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    operator = Column(String, nullable=True)
    status = Column(String, nullable=True)
    num_connectors = Column(Integer, nullable=True)
    connector_types = Column(String, nullable=True)
    date_added = Column(DateTime, nullable=True)
