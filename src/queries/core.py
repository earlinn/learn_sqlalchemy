from sqlalchemy import insert, select, text, update

from database import async_engine, sync_engine
from models import metadata_obj, workers_table


def get_sync_123():
    with sync_engine.connect() as conn:
        result = conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"sync {result.all()=}")


async def get_async_123():
    async with async_engine.connect() as conn:
        result = await conn.execute(text("SELECT 1,2,3 UNION SELECT 4,5,6"))
        print(f"async {result.all()=}")


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            statement = insert(workers_table).values(
                [{"username": "Jack"}, {"username": "Michael"}]
            )
            conn.execute(statement)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)  # SELECT * FROM workers;
            result = conn.execute(query)
            workers = result.all()
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Micha"):
        with sync_engine.connect() as conn:
            # to avoid SQL injections as we can't use f-strings (SQL injections risk)
            # statement = text("UPDATE workers SET username=:username WHERE id=:id")
            # statement = statement.bindparams(username=new_username, id=worker_id)
            statement = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            conn.execute(statement)
            conn.commit()
