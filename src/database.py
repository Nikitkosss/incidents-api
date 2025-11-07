from typing import Any

from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings as s


sql_link = (
    f"postgresql+asyncpg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_SERVER}"
    f":{s.POSTGRES_PORT}/{s.POSTGRES_DB}"
)
engine = create_async_engine(sql_link, echo=False, poolclass=NullPool)

SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, class_=AsyncSession, bind=engine
)


sql_link_sync = sql_link.replace("postgresql+asyncpg://", "postgresql://")
sync_engine = create_engine(sql_link_sync, echo=False, poolclass=NullPool)

Base: Any = declarative_base()


def create_tables_sync():
    Base.metadata.create_all(bind=sync_engine)
