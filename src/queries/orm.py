from database import Base, async_session_factory, sync_engine, sync_session_factory
from models import WorkersORM


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        sync_engine.echo = True
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_session_factory() as session:
            worker_beaver = WorkersORM(username="Jack")
            worker_wolf = WorkersORM(username="Michael")
            session.add_all([worker_beaver, worker_wolf])
            session.commit()


async def async_insert_data():
    async with async_session_factory() as session:
        worker_beaver = WorkersORM(username="Beaver")
        worker_wolf = WorkersORM(username="Wolf")
        session.add_all([worker_beaver, worker_wolf])
        await session.commit()
