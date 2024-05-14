from typing import AsyncGenerator

from redis import asyncio as aioredis
from redis.asyncio import Redis

from config_reader import Config, load_config


config: Config = load_config()


async def get_redis() -> AsyncGenerator[Redis, None]:
    """Function to get redis instance"""
    redis: Redis = aioredis.from_url(config.redis.make_connection_string())
    yield redis
