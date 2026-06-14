from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql://analista:Horus2026@postgres:5432/horus_bd"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
        autocommit = False,
        autoflush  = False,
        bind       = engine
)
