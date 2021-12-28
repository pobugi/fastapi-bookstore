from typing import AsyncGenerator

from app.db.session_async import Session as AsyncSession


async def get_db_async() -> AsyncGenerator:
    db = AsyncSession()
    try:
        yield db
    finally:
        db.close()
