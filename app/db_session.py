from typing import AsyncGenerator

from configreader import load_config
from db.Repo import Repo
from db.db import sa_sessionmaker


config = load_config()
session_factory = sa_sessionmaker(config.postgres)


async def get_session() -> AsyncGenerator[Repo, None]:
    async with session_factory() as session:
        repo: Repo = Repo(session=session)
        yield repo
