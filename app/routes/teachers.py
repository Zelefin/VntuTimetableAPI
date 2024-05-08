import logging
from typing import Dict

from fastapi import APIRouter, Depends

from app.db_session import get_session
from app.utils import update_teachers
from db.repo import Repo

teachers_router = APIRouter()


@teachers_router.post("/v0/teachers")
async def update_teachers_request(repo: Repo = Depends(get_session)) -> Dict:
    """
    Updates all teachers.
    :param repo: db repo
    :return: message (on success) or error (on failure)
    """
    try:
        await update_teachers(repo=repo)
        return {"message": "Teachers updated"}
    except Exception as e:
        logging.exception(e)
        return {"error": str(e)}
