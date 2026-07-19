from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    "postgresql+psycopg://analista:Horus2026@localhost:5432/horus_bd"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
        autocommit = False,
        autoflush  = False,
        bind       = engine
)
