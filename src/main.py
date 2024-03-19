import os
import sys

# from queries.core import SyncCore
from queries.orm import SyncORM

sys.path.insert(1, os.path.join(sys.path[0], ".."))

SyncORM.create_tables()
# SyncCore.create_tables()

SyncORM.insert_workers()
# SyncCore.insert_workers()

# SyncCore.select_workers()
# SyncCore.update_worker()

SyncORM.select_workers()
SyncORM.update_worker()
