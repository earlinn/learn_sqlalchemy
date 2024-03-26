import enum
from datetime import datetime
from typing import Annotated

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    Column,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now() + interval '1 day')")),
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

    # Можно указать на связь с worker также через backref=, но это устаревший метод,
    # backref неявно создаст в CVORM поле worker, как если бы его там не было,
    # но для ясности лучше прописывать такие связи явно с помощью back_populates
    cvs: Mapped[list["CVORM"]] = relationship(back_populates="worker")

    # в primaryjoin мы указываем дополнительный параметр для join - только parttime
    cvs_parttime: Mapped[list["CVORM"]] = relationship(
        back_populates="worker",
        primaryjoin=(
            "and_(WorkersORM.id == CVORM.worker_id, " "CVORM.workload == 'parttime')"
        ),
        order_by="CVORM.id.desc()",
    )


class WorkLoad(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class CVORM(Base):
    __tablename__ = "cvs"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int]
    workload: Mapped[WorkLoad]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped["WorkersORM"] = relationship(back_populates="cvs")

    vacancies_replied: Mapped[list["VacanciesORM"]] = relationship(
        back_populates="cvs_replied", secondary="vacancies_replies"
    )

    # переопределение этих параметров класса Base:
    repr_cols_num = 2
    repr_cols = ("created_at",)

    # можно сюда добавлять также PK и FK, но для повышения читабельности их лучше делать
    #  при объявлении соответствующих столбцов
    __table_args__ = (
        Index("title_index", "title"),
        CheckConstraint("compensation > 0", name="check_compensation_positive"),
    )


class VacanciesORM(Base):
    __tablename__ = "vacancies"

    id: Mapped[intpk]
    title: Mapped[str_256]
    compensation: Mapped[int | None]

    cvs_replied: Mapped[list["CVORM"]] = relationship(
        back_populates="vacancies_replied", secondary="vacancies_replies"
    )


class VacanciesRepliesORM(Base):
    __tablename__ = "vacancies_replies"

    cv_id: Mapped[int] = mapped_column(
        ForeignKey("cvs.id", ondelete="CASCADE"), primary_key=True
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"), primary_key=True
    )
    cover_letter: Mapped[str | None]


metadata_obj = MetaData()

# imperative mapping style
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)

cvs_table = Table(
    "cvs",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String(256)),
    Column("compensation", Integer, nullable=True),
    Column("workload", Enum(WorkLoad)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=text("TIMEZONE('utc', now())")),
    Column(
        "updated_at",
        TIMESTAMP,
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
)

vacancies_table = Table(
    "vacancies",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("compensation", Integer, nullable=True),
)
