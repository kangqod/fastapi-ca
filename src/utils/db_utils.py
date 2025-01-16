from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal, SessionLocal, async_engine


def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    async with AsyncSessionLocal() as session:
        # To Something
        await session.commit()
    await AsyncSessionLocal.remove()
    await async_engine.dispose()
