from sqlalchemy import Integer, and_, func, insert, select
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload

from database import (
    Base,
    async_engine,
    async_session_factory,
    sync_engine,
    sync_session_factory,
)
from models import CVORM, WorkersORM, WorkLoad
from schemas import WorkersRelationshipDTO


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
    def select_cvs_avg_compensation(like_language: str = "Python"):
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
                    func.avg(CVORM.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(CVORM)
                .filter(
                    and_(
                        CVORM.title.contains(like_language),
                        CVORM.compensation > 40000,
                    )
                )
                .group_by(CVORM.workload)
                .having(func.avg(CVORM.compensation).cast(Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    def insert_additional_cvs():
        with sync_session_factory() as session:
            workers = [
                {"username": "Artem"},
                {"username": "Roman"},
                {"username": "Petr"},
            ]
            cvs = [
                {
                    "title": "Python программист",
                    "compensation": 60000,
                    "workload": "fulltime",
                    "worker_id": 3,
                },
                {
                    "title": "Machine Learning Engineer",
                    "compensation": 70000,
                    "workload": "parttime",
                    "worker_id": 3,
                },
                {
                    "title": "Python Data Scientist",
                    "compensation": 80000,
                    "workload": "parttime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Analyst",
                    "compensation": 90000,
                    "workload": "fulltime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Junior Developer",
                    "compensation": 100000,
                    "workload": "fulltime",
                    "worker_id": 5,
                },
            ]
            insert_workers = insert(WorkersORM).values(workers)
            insert_resumes = insert(CVORM).values(cvs)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def join_cte_subquery_window_func():
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_workload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                c.compensation,
                c.workload,
                avg(c.compensation) OVER (PARTITION BY workload)::int
                AS avg_workload_compensation
            FROM cvs c
            JOIN workers w ON c.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC
        """
        with sync_session_factory() as session:
            c = aliased(CVORM)
            w = aliased(WorkersORM)
            subq = (
                select(
                    c,
                    w,
                    func.avg(c.compensation)
                    .over(partition_by=c.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                .join(w, c.worker_id == w.id)
                .subquery("helper1")
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label(
                    "compensation_diff"
                ),
            ).cte("helper2")
            query = select(cte).order_by(cte.c.compensation_diff.desc())
            # print(query.compile(compile_kwargs={"literal_binds": True}))
            result = session.execute(query).all()
            print(f"{result=}")

    @staticmethod
    def select_workers_with_lazy_relationship():
        with sync_session_factory() as session:
            query = select(WorkersORM)
            result = session.execute(query).scalars().all()
            worker_1_cvs = result[0].cvs
            print(worker_1_cvs)
            worker_2_cvs = result[1].cvs
            print(worker_2_cvs)

    @staticmethod
    def select_workers_with_joined_relationship():
        # joinedload - для m2o и o2o (ниже не тот случай)
        with sync_session_factory() as session:
            query = select(WorkersORM).options(joinedload(WorkersORM.cvs))
            result = session.execute(query).unique().scalars().all()
            worker_1_cvs = result[0].cvs
            print(worker_1_cvs)
            worker_2_cvs = result[1].cvs
            print(worker_2_cvs)

    @staticmethod
    def select_workers_with_selectin_relationship():
        # selectinload - для o2m (наш случай) и m2m
        with sync_session_factory() as session:
            query = select(WorkersORM).options(selectinload(WorkersORM.cvs))
            result = session.execute(query).unique().scalars().all()
            worker_1_cvs = result[0].cvs
            print(worker_1_cvs)
            worker_2_cvs = result[1].cvs
            print(worker_2_cvs)

    @staticmethod
    def select_workers_with_condition_relationship():
        with sync_session_factory() as session:
            query = select(WorkersORM).options(selectinload(WorkersORM.cvs_parttime))
            result = session.execute(query).unique().scalars().all()
            print(result)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with sync_session_factory() as session:
            query = (
                select(WorkersORM)
                .join(WorkersORM.cvs)
                .options(contains_eager(WorkersORM.cvs))
                .filter(CVORM.workload == "parttime")
            )
            result = session.execute(query).unique().scalars().all()
            print(result)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager_with_limit():
        with sync_session_factory() as session:
            subq = (
                select(CVORM.id.label("parttime_cv_id"))
                .filter(CVORM.worker_id == WorkersORM.id)
                .order_by(WorkersORM.id.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(WorkersORM)
            )
            query = (
                select(WorkersORM)
                .join(CVORM, CVORM.id.in_(subq))
                .options(contains_eager(WorkersORM.cvs))
            )
            result = session.execute(query).unique().scalars().all()
            print(result)

    @staticmethod
    def convert_workers_to_dto():
        with sync_session_factory() as session:
            query = select(WorkersORM).options(selectinload(WorkersORM.cvs)).limit(2)
            result = session.execute(query).unique().scalars().all()
            return [
                WorkersRelationshipDTO.model_validate(row, from_attributes=True)
                for row in result
            ]


# more info on limiting joinedloaded results:
# https://stackoverflow.com/questions/72096054/sqlalchemy-limit-the-joinedloaded-results


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

    @staticmethod
    async def update_worker(worker_id: int = 2, new_username: str = "Micha"):
        async with async_session_factory() as session:
            worker_michael = await session.get(WorkersORM, worker_id)
            worker_michael.username = new_username
            await session.refresh(worker_michael)
            await session.commit()

    @staticmethod
    async def insert_cvs():
        async with async_session_factory() as session:
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
            await session.commit()

    @staticmethod
    async def select_cvs_avg_compensation(like_language: str = "Python"):
        """
        select workload, avg(compensation)::int as avg_compensation
        from resumes
        where title like '%Python%' and compensation > 40000
        group by workload
        having avg(compensation) > 70000
        """
        async with async_session_factory() as session:
            query = (
                select(
                    CVORM.workload,
                    # 1 вариант использования cast
                    # cast(func.avg(CVORM.compensation), Integer)
                    # .label("avg_compensation"),
                    # 2 вариант использования cast (предпочтительный способ)
                    func.avg(CVORM.compensation)
                    .cast(Integer)
                    .label("avg_compensation"),
                )
                .select_from(CVORM)
                .filter(
                    and_(
                        CVORM.title.contains(like_language), CVORM.compensation > 40000
                    )
                )
                .group_by(CVORM.workload)
                .having(func.avg(CVORM.compensation) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.all()
            print(result[0].avg_compensation)

    @staticmethod
    async def insert_additional_cvs():
        async with async_session_factory() as session:
            workers = [
                {"username": "Artem"},
                {"username": "Roman"},
                {"username": "Petr"},
            ]
            cvs = [
                {
                    "title": "Python программист",
                    "compensation": 60000,
                    "workload": "fulltime",
                    "worker_id": 3,
                },
                {
                    "title": "Machine Learning Engineer",
                    "compensation": 70000,
                    "workload": "parttime",
                    "worker_id": 3,
                },
                {
                    "title": "Python Data Scientist",
                    "compensation": 80000,
                    "workload": "parttime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Analyst",
                    "compensation": 90000,
                    "workload": "fulltime",
                    "worker_id": 4,
                },
                {
                    "title": "Python Junior Developer",
                    "compensation": 100000,
                    "workload": "fulltime",
                    "worker_id": 5,
                },
            ]
            insert_workers = insert(WorkersORM).values(workers)
            insert_resumes = insert(CVORM).values(cvs)
            await session.execute(insert_workers)
            await session.execute(insert_resumes)
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func():
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_workload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                c.compensation,
                c.workload,
                avg(c.compensation) OVER (PARTITION BY workload)::int
                AS avg_workload_compensation
            FROM cvs c
            JOIN workers w ON c.worker_id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC
        """
        async with async_session_factory() as session:
            c = aliased(CVORM)
            w = aliased(WorkersORM)
            subq = (
                select(
                    c,
                    w,
                    func.avg(c.compensation)
                    .over(partition_by=c.workload)
                    .cast(Integer)
                    .label("avg_workload_compensation"),
                )
                .join(w, c.worker_id == w.id)
                .subquery("helper1")
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_compensation,
                (subq.c.compensation - subq.c.avg_workload_compensation).label(
                    "compensation_diff"
                ),
            ).cte("helper2")
            query = select(cte).order_by(cte.c.compensation_diff.desc())
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = await session.execute(query)
            result = res.scalars().all()
            print(f"{result=}")
