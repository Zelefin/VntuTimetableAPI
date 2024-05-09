import logging

from aiohttp import ClientError
from apscheduler.job import Job  # type: ignore
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.exceptions.jet_status_exception import JetIQStatusCodeError
from app.utils import (
    update_faculties,
    update_groups,
    update_teachers,
    update_groups_lessons,
)
from db.repo import Repo


async def update_faculties_table(
    session_factory: async_sessionmaker[AsyncSession], redis: Redis, retry_task: Job
) -> None:
    """Task to update faculties table."""
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            await update_faculties(repo=repo, redis=redis)
        retry_task.pause()
    except JetIQStatusCodeError as e:
        logging.exception("Error while updating faculties table. Exception: %s", e)
        retry_task.resume()
    except ClientError as e:
        logging.error("Got client error while getting faculties: %s", e)
        retry_task.resume()


async def update_groups_table(
    session_factory: async_sessionmaker[AsyncSession], redis: Redis, retry_task: Job
) -> None:
    """Task to update groups table."""
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            faculties: list[int] = [
                faculty.id for faculty in await repo.get_faculties()
            ]
            await update_groups(repo=repo, redis=redis, faculties=faculties)
        retry_task.pause()
    except JetIQStatusCodeError as e:
        logging.exception("Error while updating groups table. Exception: %s", e)
        retry_task.resume()
    except ClientError as e:
        logging.error(
            "Got client error while getting groups error: %s",
            e,
        )
        retry_task.resume()


# async def update_teachers_table(
#     session_factory: async_sessionmaker[AsyncSession], retry_task: Job
# ) -> None:
#     try:
#         async with session_factory() as session:
#             repo: Repo = Repo(session=session)
#             await update_teachers(repo=repo)
#         retry_task.pause()
#     except Exception as e:
#         logging.info("Error while updating teachers table")
#         logging.exception(e)
#         retry_task.resume()


async def update_groups_lessons_table(
    session_factory: async_sessionmaker[AsyncSession], redis: Redis, retry_task: Job
) -> None:
    """Task to update groups lessons table."""
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            groups_ids: list[int] = [group.id for group in await repo.get_groups()]
            await update_groups_lessons(repo=repo, redis=redis, groups_ids=groups_ids)
        retry_task.pause()
    except IntegrityError:
        logging.info("Error while updating groups lessons table. Problem with teachers")
        await update_teachers(repo=repo)
        logging.info("Updated teachers")
        await update_groups_lessons(repo=repo, redis=redis, groups_ids=groups_ids)
        logging.info("Updated groups lessons")
    except JetIQStatusCodeError as e:
        logging.exception(
            "Error while updating groups lessons table. Problem NOT with teachers. Exception: %s",
            e,
        )
        retry_task.resume()
    except ClientError as e:
        logging.error(
            "Got client error while getting group schedule; error - %s",
            e,
        )
        retry_task.resume()
