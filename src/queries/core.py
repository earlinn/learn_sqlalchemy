from sqlalchemy import text

from database import async_engine, sync_engine
from models import metadata_obj


def get_sync_123():
    with sync_engine.connect() as conn:
        result = conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"sync {result.all()=}")


async def get_async_123():
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"async {result.all()=}")


def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = True


def insert_data():
    with sync_engine.connect() as conn:
        statement = "INSERT INTO workers (username) VALUES ('Bobr'), ('Volk');"
        conn.execute(text(statement))
        conn.commit()
