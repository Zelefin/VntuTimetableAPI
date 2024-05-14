import logging
from typing import Dict

from aiohttp import ClientError
from fastapi import APIRouter, Depends

from app.db_session import get_session
from app.exceptions.jet_status_exception import JetIQStatusCodeError
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
    except JetIQStatusCodeError as e:
        logging.exception("/teachers status error: %s", e)
        return {"error": str(e)}
    except ClientError as e:
        logging.exception(
            "Got client error on post /teachers endpoint. Exception: %s", e
        )
        return {"error": "ClientError"}
