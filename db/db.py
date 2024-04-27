from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from configreader import Postgres


def make_connection_string(db: Postgres, async_fallback: bool = False) -> str:
    result = f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.db}"
    if async_fallback:
        result += "?async_fallback=True"
    return result


def create_engine(connection_string: str, echo: bool = False):
    engine = create_async_engine(
        connection_string,
        query_cache_size=1200,
        pool_size=20,
        max_overflow=200,
        future=True,
        echo=echo,
    )
    return engine


def sa_sessionmaker(
    db: Postgres, echo: bool = False
) -> async_sessionmaker[AsyncSession]:
    engine = create_engine(make_connection_string(db), echo=echo)
    session_pool = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False, class_=AsyncSession
    )
    return session_pool
