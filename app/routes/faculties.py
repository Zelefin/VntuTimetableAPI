import json
import logging
from typing import Sequence, Dict

from aiohttp import ClientError
from fastapi import APIRouter, Depends
from redis.asyncio import Redis

from app.db_session import get_session
from app.exceptions.jet_status_exception import JetIQStatusCodeError
from app.redis_session import get_redis
from app.utils import update_faculties, update_groups
from db.repo import Repo
from db.models import Faculty

faculty_router = APIRouter()


@faculty_router.get("/v0/faculties")
async def get_faculties_with_groups(
    repo: Repo = Depends(get_session), redis: Redis = Depends(get_redis)
) -> Dict:
    """
    Returns list of all faculties with all groups of particular faculty
    :param repo: db repo
    :param redis: redis
    :return: list of all faculties and their groups
    """
    if cached_response := await redis.get(name="faculties"):
        return {"cached": True, "data": json.loads(cached_response)}

    faculties: Sequence[Faculty] = await repo.get_faculties()
    response = [
        {
            "id": faculty.id,
            "name": faculty.name,
            "groups": [
                {"id": group.id, "name": group.name}
                for group in await repo.get_groups_of_faculty(faculty_id=faculty.id)
            ],
        }
        for faculty in faculties
    ]

    await redis.set(name="faculties", value=json.dumps(response), ex=10_800)

    return {"cached": False, "data": response}


@faculty_router.post("/v0/faculties")
async def update_faculties_request(
    repo: Repo = Depends(get_session), redis: Redis = Depends(get_redis)
) -> Dict:
    """
    Updates faculties list
    :param repo: db repo
    :param redis: redis instance
    :return: message (in case of success) or error (in case of failure)
    """
    try:
        await update_faculties(repo=repo, redis=redis)
        return {"message": "Faculties list updated"}
    except JetIQStatusCodeError as e:
        logging.exception("/faculties status error: %s", e)
        return {"error": str(e)}
    except ClientError as e:
        logging.exception(
            "Got client error on post /faculties endpoint. Exception: %s", e
        )
        return {"error": "ClientError"}


@faculty_router.post("/v0/faculties/groups")
async def update_faculties_groups(
    repo: Repo = Depends(get_session), redis: Redis = Depends(get_redis)
):
    """
    Updates faculties groups list.
    :param repo: db repo.
    :param redis: redis instance.
    :return: message (in case of success) or error (in case of failure)
    """
    try:
        faculties: list[int] = [faculty.id for faculty in await repo.get_faculties()]
        await update_groups(repo=repo, redis=redis, faculties=faculties)
        return {"message": "Groups list updated"}
    except JetIQStatusCodeError as e:
        logging.exception("/faculties/groups status error: %s", e)
        return {"error": str(e)}
    except ClientError as e:
        logging.exception(
            "Got client error on post /faculties/groups endpoint. Exception: %s", e
        )
        return {"error": "ClientError"}
