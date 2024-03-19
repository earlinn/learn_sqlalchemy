from sqlalchemy import select

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
            worker_jack = WorkersORM(username="Jack")
            worker_michael = WorkersORM(username="Michael")
            session.add_all([worker_jack, worker_michael])
            session.flush()
            session.commit()

    @staticmethod
    def select_workers():
        with sync_session_factory() as session:
            # worker_id = 1
            # worker_jack = session.get(WorkersORM, worker_id)
            query = select(WorkersORM)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Micha"):
        with sync_session_factory() as session:
            worker_michael = session.get(WorkersORM, worker_id)
            worker_michael.username = new_username
            session.refresh(worker_michael)
            session.commit()


async def async_insert_data():
    async with async_session_factory() as session:
        worker_jack = WorkersORM(username="Jack")
        worker_michael = WorkersORM(username="Michael")
        session.add_all([worker_jack, worker_michael])
        await session.commit()
