from sqlalchemy import inspect

from database import SessionLocal


def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
