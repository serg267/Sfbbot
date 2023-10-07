from typing import Union

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker


def url_object() -> URL:
    """create url object with db connection variables"""
    url = URL.create(
        "postgresql+asyncpg",
        username="postgres",  # better to use env variables
        password="Nikola27",  # plain (unescaped) text
        host='localhost',  # better to use env variables
        port=5432,  # better to use env variables
        database="postgres",  # better to use env variables
    )
    return url


def create_the_engine(url: Union[URL, str]) -> AsyncEngine:
    """create connection to the db"""
    return create_async_engine(url=url, echo=True)


def get_session_maker(async_engine: AsyncEngine) -> async_sessionmaker:
    """to record and read data from the db"""
    return async_sessionmaker(async_engine, class_=AsyncSession)


def proceed_schemas(session: AsyncSession, metadata) -> None:
    with session.begin():
        session.run_sync(metadata.create_all)


