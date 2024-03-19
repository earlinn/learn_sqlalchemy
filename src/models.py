from sqlalchemy import Column, Integer, MetaData, String, Table

metadata_obj = MetaData()


# imperative mapping style
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
