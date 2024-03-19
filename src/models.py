import enum
from datetime import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]
updated_at = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
]


class WorkersORM(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str]


class WorkLoad(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class CVORM(Base):
    __tablename__ = "cvs"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
