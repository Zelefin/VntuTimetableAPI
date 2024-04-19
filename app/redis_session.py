from typing import AsyncGenerator

from redis import asyncio as aioredis
from redis.asyncio import Redis


async def get_redis() -> AsyncGenerator[Redis, None]:
    redis: Redis = aioredis.from_url("redis://localhost:6379/0")
    yield redis
