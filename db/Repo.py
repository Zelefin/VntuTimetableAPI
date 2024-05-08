from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Lesson, Group, Faculty, Teacher


class Repo:
    """Database repo"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def check_group(self, group_id: int) -> bool:
        """Check whether a group exists in the database."""
        return bool(
            await self.session.scalar(select(Group).where(Group.id == group_id))
        )

    async def get_group_lessons(self, group_id: int) -> Sequence[Lesson]:
        """Get the group's lessons."""
        return (
            await self.session.scalars(
                select(Lesson)
                .options(joinedload(Lesson.teacher))
                .where(Lesson.group_id == group_id)
            )
        ).all()

    async def get_faculties(self) -> Sequence[Faculty]:
        """Get list of faculties."""
        return (await self.session.scalars(select(Faculty))).all()

    async def get_faculty(self, faculty_id: int) -> Faculty | None:
        """Get specific faculty."""
        return (
            await self.session.execute(select(Faculty).where(Faculty.id == faculty_id))
        ).scalar_one_or_none()

    async def get_groups(self) -> Sequence[Group]:
        """Get all groups."""
        return (await self.session.scalars(select(Group))).all()

    async def get_group(self, group_id: int) -> Group | None:
        """Get specific group."""
        return (
            await self.session.execute(select(Group).where(Group.id == group_id))
        ).scalar_one_or_none()

    async def get_groups_of_faculty(self, faculty_id: int) -> Sequence[Group]:
        """Get all groups of faculty."""
        return (
            await self.session.scalars(
                select(Group).where(Group.faculty_id == faculty_id)
            )
        ).all()

    async def get_teacher_by_id(self, teacher_id: int) -> Teacher | None:
        """Get specific teacher by id."""
        return (
            await self.session.execute(select(Teacher).where(Teacher.id == teacher_id))
        ).scalar_one_or_none()

    async def get_teacher_by_name(self, teacher_name: str) -> Teacher | None:
        """Get specific teacher by name."""
        return (
            await self.session.execute(
                select(Teacher).where(Teacher.name == teacher_name)
            )
        ).scalar()
