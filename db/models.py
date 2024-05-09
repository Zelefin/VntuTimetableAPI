import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, UUID, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all models."""


class Lesson(Base):
    """Lesson model."""

    __tablename__ = "lessons"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group: Mapped["Group"] = relationship(back_populates="lessons")
    num: Mapped[int] = mapped_column()
    auditory: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()
    subgroup: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teacher"] = relationship(back_populates="lessons")
    begin: Mapped[datetime] = mapped_column(DateTime)
    end: Mapped[datetime] = mapped_column(DateTime)
    dow: Mapped[str] = mapped_column()
    week_num: Mapped[int] = mapped_column()
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()  # pylint: disable=not-callable
    )

    def to_dict(self) -> dict:
        """Formatting lesson object to dictionary."""
        formatted_lesson: dict = {
            "num": self.num,
            "auditory": self.auditory,
            "type": self.type,
            "subgroup": self.subgroup,
            "name": self.name,
            "teacher": {
                "id": self.teacher.id,
                "name": self.teacher.name,
            },
            "begin": self.begin.strftime("%H:%M"),
            "end": self.end.strftime("%H:%M"),
            "added_at": self.added_at.strftime("%d/%m/%Y, %H:%M:%S"),
        }

        return formatted_lesson


class Teacher(Base):
    """Teacher model."""

    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="teacher")
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()  # pylint: disable=not-callable
    )


class Group(Base):
    """Group model."""

    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="group")
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"))
    faculty: Mapped["Faculty"] = relationship(back_populates="groups")
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()  # pylint: disable=not-callable
    )


class Faculty(Base):
    """Faculty model."""

    __tablename__ = "faculties"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    groups: Mapped[List["Group"]] = relationship(back_populates="faculty")
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()  # pylint: disable=not-callable
    )
