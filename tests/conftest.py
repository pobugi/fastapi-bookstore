from asyncio import get_event_loop
from typing import Any, AsyncGenerator

import pytest
from app.api.deps import get_db_async
from app.core.config import settings
from app.db.base_class import Base
from app.main import app
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.TEST_DATABASE_URL)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_test_db_async() -> AsyncGenerator:
    db = Session()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture(scope="session")
async def test_app() -> AsyncGenerator:
    app.dependency_overrides[get_db_async] = get_test_db_async

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(app=app, base_url=settings.BASE_URL) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop() -> Any:
    loop = get_event_loop()
    yield loop
    loop.close()
