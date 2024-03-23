from typing import Annotated

from sqlalchemy import String, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

sync_engine = create_engine(url=settings.database_url_psycopg, echo=True)
async_engine = create_async_engine(url=settings.database_url_asyncpg, echo=True)

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    repr_cols_num = 3  # сколько колонок вывести на печать
    repr_cols = tuple()  # для вывода дополнительных колонок

    def __repr__(self) -> str:
        """
        Relationships не используются в repr, т.к. могут вести к неожиданным подгрузкам.
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"<{self.__class__.__name__} {','.join(cols)}>"
