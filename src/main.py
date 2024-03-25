import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from queries.core import AsyncCore, SyncCore
from queries.orm import AsyncORM, SyncORM

sys.path.insert(1, os.path.join(sys.path[0], ".."))


async def main():
    if "--core" in sys.argv and "--sync" in sys.argv:
        SyncCore.create_tables()
        SyncCore.insert_workers()
        SyncCore.select_workers()
        SyncCore.update_worker()
        SyncCore.insert_cvs()
        SyncCore.select_cvs_avg_compensation()
        SyncCore.insert_additional_cvs()
        SyncCore.join_cte_subquery_window_func()

    elif "--core" in sys.argv and "--async" in sys.argv:
        await AsyncCore.create_tables()
        await AsyncCore.insert_workers()
        await AsyncCore.select_workers()
        await AsyncCore.update_worker()
        await AsyncCore.insert_cvs()
        await AsyncCore.select_cvs_avg_compensation()
        await AsyncCore.insert_additional_cvs()
        await AsyncCore.join_cte_subquery_window_func()

    elif "--orm" in sys.argv and "--sync" in sys.argv:
        SyncORM.create_tables()
        SyncORM.insert_workers()
        SyncORM.select_workers()
        SyncORM.update_worker()
        SyncORM.insert_cvs()
        SyncORM.select_cvs_avg_compensation()
        SyncORM.insert_additional_cvs()
        SyncORM.join_cte_subquery_window_func()
        SyncORM.select_workers_with_lazy_relationship()
        SyncORM.select_workers_with_joined_relationship()
        SyncORM.select_workers_with_selectin_relationship()
        SyncORM.select_workers_with_condition_relationship()
        SyncORM.select_workers_with_condition_relationship_contains_eager()
        SyncORM.select_workers_with_condition_relationship_contains_eager_with_limit()
        SyncORM.insert_vacancies_and_replies()
        SyncORM.select_cvs_with_all_relationships()

    elif "--orm" in sys.argv and "--async" in sys.argv:
        await AsyncORM.create_tables()
        await AsyncORM.insert_workers()
        await AsyncORM.select_workers()
        await AsyncORM.update_worker()
        await AsyncORM.insert_cvs()
        await AsyncORM.select_cvs_avg_compensation()
        await AsyncORM.insert_additional_cvs()
        await AsyncORM.join_cte_subquery_window_func()


def create_fastapi_app():
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=["*"])

    @app.get("/workers")
    async def get_workers():
        return SyncORM.convert_workers_to_dto()

    return app


app = create_fastapi_app()


if __name__ == "__main__":
    asyncio.run(main())
    uvicorn.run(app="src.main:app", reload=True)
