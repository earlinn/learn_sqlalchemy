import asyncio
import os
import sys

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

    elif "--core" in sys.argv and "--async" in sys.argv:
        await AsyncCore.create_tables()
        await AsyncCore.insert_workers()
        await AsyncCore.select_workers()
        await AsyncCore.update_worker()
        await AsyncCore.insert_cvs()
        await AsyncCore.select_cvs_avg_compensation()

    elif "--orm" in sys.argv and "--sync" in sys.argv:
        SyncORM.create_tables()
        SyncORM.insert_workers()
        SyncORM.select_workers()
        SyncORM.update_worker()
        SyncORM.insert_cvs()
        SyncORM.select_cvs_avg_compensation()
        SyncORM.insert_additional_cvs()
        SyncORM.join_cte_subquery_window_func()

    elif "--orm" in sys.argv and "--async" in sys.argv:
        await AsyncORM.create_tables()
        await AsyncORM.insert_workers()
        await AsyncORM.select_workers()
        await AsyncORM.update_worker()
        await AsyncORM.insert_cvs()
        await AsyncORM.select_cvs_avg_compensation()


if __name__ == "__main__":
    asyncio.run(main())
