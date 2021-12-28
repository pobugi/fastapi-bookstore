from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)

Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with Session() as session:
        return await session
