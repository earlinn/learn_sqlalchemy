from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text

from config import settings


engine = create_engine(url=settings.DATABASE_URL_psycopg, echo=True)

with engine.connect() as conn:
    result = conn.execute(text("SELECT VERSION()"))
    print(f"{result=}")
