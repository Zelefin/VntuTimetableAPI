from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Lesson, Group, Faculty


class Repo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check_group(self, group_id: int) -> bool:
        return True if await self.session.scalar(select(Group).where(Group.id == group_id)) else False

    async def get_group_lessons(self, group_id: int) -> Sequence[Lesson]:
        return (
            await self.session.scalars(
                select(Lesson).options(joinedload(Lesson.teacher)).where(Lesson.group_id == group_id)
            )
        ).all()

    async def get_faculties(self) -> Sequence[Faculty]:
        return (await self.session.scalars(select(Faculty))).all()

    async def get_groups_of_faculty(self, faculty_id: int) -> Sequence[Group]:
        return (await self.session.scalars(select(Group).where(Group.faculty_id == faculty_id))).all()
