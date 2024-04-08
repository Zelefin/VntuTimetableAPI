from typing import Sequence, Dict

from fastapi import APIRouter, Depends

from app.db_session import get_session
from db.Repo import Repo
from db.models import Faculty

faculty_router = APIRouter()


@faculty_router.get("/v0/faculties")
async def get_faculties_with_groups(repo: Repo = Depends(get_session)) -> Dict:
    """
    Returns list of all faculties with all groups of particular faculty
    :param repo: db repo
    :return: list of all faculties and their groups
    """
    faculties: Sequence[Faculty] = await repo.get_faculties()
    return {
        "data": [
            {"id": faculty.id, "name": faculty.name, "groups": [
                {"id": group.id, "name": group.name} for group in
                await repo.get_groups_of_faculty(faculty_id=faculty.id)
            ]
             } for faculty in faculties
        ]
    }
