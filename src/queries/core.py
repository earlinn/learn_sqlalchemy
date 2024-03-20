from sqlalchemy import Integer, and_, func, insert, select, text, update

from database import async_engine, sync_engine
from models import WorkLoad, cvs_table, metadata_obj, workers_table


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

    @staticmethod
    def insert_cvs():
        with sync_engine.connect() as conn:
            cvs = [
                {
                    "title": "Python Junior Developer",
                    "compensation": 50000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Разработчик",
                    "compensation": 150000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Data Engineer",
                    "compensation": 250000,
                    "workload": WorkLoad.parttime,
                    "worker_id": 2,
                },
                {
                    "title": "Data Scientist",
                    "compensation": 300000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 2,
                },
            ]
            statement = insert(cvs_table).values(cvs)
            conn.execute(statement)
            conn.commit()

    @staticmethod
    def select_cvs_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        with sync_engine.connect() as conn:
            query = (
                select(
                    cvs_table.c.workload,
                    func.avg(cvs_table.c.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(cvs_table)
                .filter(
                    and_(
                        cvs_table.c.title.contains(like_language),
                        cvs_table.c.compensation > 40000,
                    )
                )
                .group_by(cvs_table.c.workload)
                .having(func.avg(cvs_table.c.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = conn.execute(query)
            result = res.all()
            print(result[0].avg_compensation)


class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)

    @staticmethod
    async def insert_workers():
        async with async_engine.connect() as conn:
            statement = insert(workers_table).values(
                [{"username": "Jack"}, {"username": "Michael"}]
            )
            await conn.execute(statement)
            await conn.commit()

    @staticmethod
    async def select_workers():
        async with async_engine.connect() as conn:
            query = select(workers_table)  # SELECT * FROM workers;
            result = await conn.execute(query)
            workers = result.all()
            print(f"{workers=}")

    @staticmethod
    async def update_worker(worker_id: int = 2, new_username: str = "Micha"):
        async with async_engine.connect() as conn:
            # to avoid SQL injections as we can't use f-strings (SQL injections risk)
            # statement = text("UPDATE workers SET username=:username WHERE id=:id")
            # statement = statement.bindparams(username=new_username, id=worker_id)
            statement = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            await conn.execute(statement)
            await conn.commit()

    @staticmethod
    async def insert_cvs():
        async with async_engine.connect() as conn:
            cvs = [
                {
                    "title": "Python Junior Developer",
                    "compensation": 50000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Разработчик",
                    "compensation": 150000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 1,
                },
                {
                    "title": "Python Data Engineer",
                    "compensation": 250000,
                    "workload": WorkLoad.parttime,
                    "worker_id": 2,
                },
                {
                    "title": "Data Scientist",
                    "compensation": 300000,
                    "workload": WorkLoad.fulltime,
                    "worker_id": 2,
                },
            ]
            statement = insert(cvs_table).values(cvs)
            await conn.execute(statement)
            await conn.commit()

    @staticmethod
    async def select_cvs_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        async with async_engine.connect() as conn:
            query = (
                select(
                    cvs_table.c.workload,
                    func.avg(cvs_table.c.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(cvs_table)
                .filter(
                    and_(
                        cvs_table.c.title.contains(like_language),
                        cvs_table.c.compensation > 40000,
                    )
                )
                .group_by(cvs_table.c.workload)
                .having(func.avg(cvs_table.c.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await conn.execute(query)
            result = res.all()
            print(result[0].avg_compensation)
