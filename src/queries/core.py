from sqlalchemy import text

from database import async_engine, sync_engine


def get_sync_123():
    with sync_engine.connect() as conn:
        result = conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"sync {result.all()=}")


async def get_async_123():
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"async {result.all()=}")
