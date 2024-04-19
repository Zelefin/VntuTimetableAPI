import logging

from sqlalchemy.orm import sessionmaker

from app.utils import update_faculties, update_groups, update_teachers, update_groups_lessons
from db.Repo import Repo


async def update_faculties_table(session_factory: sessionmaker) -> None:
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            await update_faculties(repo=repo)
    except Exception as e:
        logging.info("Error while updating faculties table")
        logging.exception(e)


async def update_groups_table(session_factory: sessionmaker) -> None:
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            faculties: dict[int, str] = {
                faculty.id: faculty.name for faculty in await Repo(session=session).get_faculties()
            }
            await update_groups(repo=repo, faculties=faculties)
    except Exception as e:
        logging.info("Error while updating groups table")
        logging.exception(e)


async def update_teachers_table(session_factory: sessionmaker) -> None:
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            await update_teachers(repo=repo)
    except Exception as e:
        logging.info("Error while updating teachers table")
        logging.exception(e)


async def update_groups_lessons_table(session_factory: sessionmaker) -> None:
    try:
        async with session_factory() as session:
            repo: Repo = Repo(session=session)
            # we can't skip updating teachers, because each lesson has relationship with teacher
            # if there is lesson with new teacher it will cause exception
            await update_teachers(repo=repo)
            groups_ids: list[int] = [group.id for group in await Repo(session=session).get_groups()]
            await update_groups_lessons(repo=repo, groups_ids=groups_ids)
    except Exception as e:
        logging.info("Error while updating groups lessons table")
        logging.exception(e)
