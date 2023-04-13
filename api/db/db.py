import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"
)

engine = create_engine(  # Solo SQLALCHEMY_DATABASE_URL para Postgresql
    SQLALCHEMY_DATABASE_URL
    # , connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    Get a database session.

    Yields:
        Generator: A generator that returns the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
