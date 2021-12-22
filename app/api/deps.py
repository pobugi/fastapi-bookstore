from typing import Generator

from app.db.session import Session


def get_db() -> Generator:
    try:
        db = Session()
        yield db
    finally:
        db.close()
