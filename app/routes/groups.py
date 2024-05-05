import json
import logging
from typing import Sequence, List, Dict

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError

from app.db_session import get_session
from app.redis_session import get_redis
from app.utils import update_group_lessons, update_groups_lessons, update_teachers
from app.misc.gen_date import gen_weeks_dates
from db.Repo import Repo
from db.models import Lesson

group_router = APIRouter()
days_dict: Dict[str, int] = {
    "Пн": 0,
    "Вт": 1,
    "Ср": 2,
    "Чт": 3,
    "Пт": 4,
    "Сб": 5,
    "Нд": 6,
}


@group_router.get("/v0/groups/{group_id}")
async def get_group_timetable(
    group_id: int,
    repo: Repo = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> Dict:
    """
    Returns timetable for the given group. First and second week
    :param group_id: id of the group
    :param repo: db repo
    :param redis: redis
    :return: timetable for the first and second week or 'group not found' if group is not in db
    """
    if not await repo.check_group(group_id=group_id):
        return {"message": "Group not found"}

    if cached_response := await redis.get(str(group_id)):
        return {"cached": True, "data": json.loads(cached_response)}

    lessons: Sequence[Lesson] = await repo.get_group_lessons(group_id=group_id)
    first_week_dates, second_week_dates = gen_weeks_dates()
    first_week: List[Dict[str, str | List]] = [
        {"day": day_name, "date": first_week_dates[day_num], "lessons": []}
        for day_name, day_num in days_dict.items()
    ]  # 7 days of the week
    second_week: List[Dict[str, str | List]] = [
        {"day": day_name, "date": second_week_dates[day_num], "lessons": []}
        for day_name, day_num in days_dict.items()
    ]  # 7 days of the week
    for lesson in lessons:
        if lesson.week_num == 1:
            # sorry mypy, but that's for sure a list
            first_week[days_dict[lesson.dow]]["lessons"].append(lesson.to_json())  # type: ignore
        else:
            second_week[days_dict[lesson.dow]]["lessons"].append(lesson.to_json())  # type: ignore

    response = {"firstWeek": first_week, "secondWeek": second_week}
    await redis.set(str(group_id), json.dumps(response), ex=10_800)

    return {"cached": False, "data": response}


@group_router.post("/v0/groups/{group_id}")
async def update_group_timetable(
    group_id: int,
    repo: Repo = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> Dict:
    """
    Updates timetable for specific group
    :param group_id: id of the group to update
    :param repo: db repo
    :param redis: redis
    :return: message or error
    """
    if not await repo.check_group(group_id=group_id):
        return {"message": "Group not found"}
    try:
        await update_group_lessons(group_id=group_id, repo=repo)
        await redis.delete(str(group_id))
        return {"message": "Group lessons updated"}
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}


@group_router.post("/v0/groups")
async def update_groups_request(
    repo: Repo = Depends(get_session), redis: Redis = Depends(get_redis)
) -> Dict:
    """
    Updates timetable for all groups
    :param repo: db repo
    :param redis: redis
    :return: message or error
    """
    try:
        if await redis.get("update_all_groups"):
            return {
                "message": f"Groups already updated. Timout: {await redis.ttl('update_all_groups')}"
            }
        await redis.set("update_all_groups", 1, ex=3600)
        groups_ids: list[int] = [group.id for group in await repo.get_groups()]
        try:
            await update_groups_lessons(repo=repo, redis=redis, groups_ids=groups_ids)
        except IntegrityError:
            logging.info(
                "Error while updating groups lessons table. Problem with teachers"
            )
            await update_teachers(repo=repo)
            logging.info("Updated teachers")
            await update_groups_lessons(repo=repo, redis=redis, groups_ids=groups_ids)
            logging.info("Updated groups lessons")
        return {"message": "Groups updated"}
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}
