from typing import AsyncGenerator

from redis import asyncio as aioredis
from redis.asyncio import Redis

from configreader import Config, load_config


config: Config = load_config()


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis: Redis = aioredis.from_url(
        f"redis://{config.redis.host}:{config.redis.port}/{config.redis.db}"
    )
    yield redis
