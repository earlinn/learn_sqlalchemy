import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text

from config import settings


sync_engine = create_engine(url=settings.DATABASE_URL_psycopg, echo=False)
async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=False)

with sync_engine.connect() as conn:
    result = conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
    print(f"sync {result.all()=}")


async def get_123():
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"async {result.all()=}")


asyncio.run(get_123())
