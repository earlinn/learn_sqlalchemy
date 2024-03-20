from sqlalchemy import Integer, and_, cast, func, select

from database import (
    Base,
    async_engine,
    async_session_factory,
    sync_engine,
    sync_session_factory,
)
from models import CVORM, WorkersORM, WorkLoad


class SyncORM:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
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

    @staticmethod
    def insert_cvs():
        with sync_session_factory() as session:
            cv_jack_1 = CVORM(
                title="Python Junior Developer",
                compensation=50000,
                workload=WorkLoad.fulltime,
                worker_id=1,
            )
            cv_jack_2 = CVORM(
                title="Python Разработчик",
                compensation=150000,
                workload=WorkLoad.fulltime,
                worker_id=1,
            )
            cv_michael_1 = CVORM(
                title="Python Data Engineer",
                compensation=250000,
                workload=WorkLoad.parttime,
                worker_id=2,
            )
            cv_michael_2 = CVORM(
                title="Data Scientist",
                compensation=300000,
                workload=WorkLoad.fulltime,
                worker_id=2,
            )
            session.add_all([cv_jack_1, cv_jack_2, cv_michael_1, cv_michael_2])
            session.commit()

    @staticmethod
    def select_cvs_avg_compendation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        with sync_session_factory() as session:
            query = (
                select(
                    CVORM.workload,
                    cast(func.avg(CVORM.compensation), Integer).label(
                        "avg_compensation"
                    ),
                )
                .select_from(CVORM)
                .filter(
                    and_(
                        CVORM.title.contains(like_language),
                        CVORM.compensation > 40000,
                    )
                )
                .group_by(CVORM.workload)
                .having(cast(func.avg(CVORM.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_workers():
        async with async_session_factory() as session:
            worker_jack = WorkersORM(username="Jack")
            worker_michael = WorkersORM(username="Michael")
            session.add_all([worker_jack, worker_michael])
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_workers():
        async with async_session_factory() as session:
            query = select(WorkersORM)
            result = await session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")
