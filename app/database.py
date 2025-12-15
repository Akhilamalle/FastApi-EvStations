import os
import csv
from pathlib import Path
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

_engine = None
_SessionLocal = None

DEFAULT_DB = "sqlite:///./ev_stations.db"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DB)


def get_engine(database_url: Optional[str] = None):
    global _engine
    url = database_url or get_database_url()
    if _engine is None or str(_engine.url) != url:
        _engine = create_engine(url, connect_args={"check_same_thread": False} if url.startswith("sqlite") else {})
    return _engine


def get_sessionmaker(database_url: Optional[str] = None):
    global _SessionLocal
    engine = get_engine(database_url)
    if _SessionLocal is None or _SessionLocal.kw.get('bind') is not engine:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal


def init_db(create_tables=True, database_url: Optional[str] = None):
    """Create DB tables and load initial sample data from bundled CSV if DB empty."""
    from .models import Base, EVStation

    engine = get_engine(database_url)
    if create_tables:
        Base.metadata.create_all(bind=engine)

    # load sample CSV if table empty
    Session = get_sessionmaker(database_url)
    session = Session()
    try:
        exists = session.query(EVStation).first()
        if not exists:
            data_path = Path(__file__).parent / "data" / "ev_stations_2025.csv"
            if data_path.exists():
                with open(data_path, newline='', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = []
                    for r in reader:
                        # transform fields
                        try:
                            lat = float(r.get('lat')) if r.get('lat') else None
                        except Exception:
                            lat = None
                        try:
                            lon = float(r.get('lon')) if r.get('lon') else None
                        except Exception:
                            lon = None
                        try:
                            num_conn = int(r.get('num_connectors')) if r.get('num_connectors') else None
                        except Exception:
                            num_conn = None
                        date_added = None
                        if r.get('date_added'):
                            try:
                                # ISO format parsing
                                date_added = datetime.fromisoformat(r.get('date_added').replace('Z', '+00:00'))
                            except Exception:
                                date_added = None

                        station = EVStation(
                            id=int(r['id']) if r.get('id') else None,
                            title=r.get('title'),
                            address=r.get('address'),
                            town=r.get('town'),
                            state=r.get('state'),
                            postcode=r.get('postcode'),
                            country=r.get('country'),
                            lat=lat,
                            lon=lon,
                            operator=r.get('operator'),
                            status=r.get('status'),
                            num_connectors=num_conn,
                            connector_types=r.get('connector_types'),
                            date_added=date_added,
                        )
                        rows.append(station)
                    if rows:
                        session.bulk_save_objects(rows)
                        session.commit()
    finally:
        session.close()
