from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from config_reader import load_config, Config
from db.Repo import Repo
from db.db import sa_sessionmaker


config: Config = load_config()
session_factory: async_sessionmaker[AsyncSession] = sa_sessionmaker(config.postgres)


async def get_session() -> AsyncGenerator[Repo, None]:
    """Function to get a Repo"""
    async with session_factory() as session:
        repo: Repo = Repo(session=session)
        yield repo
