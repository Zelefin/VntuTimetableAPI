from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker

from configreader import load_config, Config
from db.Repo import Repo
from db.db import sa_sessionmaker


config: Config = load_config()
session_factory: sessionmaker = sa_sessionmaker(config.postgres)


async def get_session() -> AsyncGenerator[Repo, None]:
    async with session_factory() as session:
        repo: Repo = Repo(session=session)
        yield repo
