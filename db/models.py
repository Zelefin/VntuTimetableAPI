import uuid
from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Lesson(Base):
    __tablename__ = 'lessons'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    date: Mapped[datetime] = mapped_column(DateTime)
    dow: Mapped[str] = mapped_column()
    week_num: Mapped[int] = mapped_column()

    def to_json(self) -> dict:
        formatted_lesson: dict = {
            "date": self.date.strftime('%d.%m'),
            "num": self.num,
            "auditory": self.auditory,
            "type": self.type,
            "subgroup": self.subgroup,
            "name": self.name,
            "teacher": {
                "id": self.teacher.id,
                "name": self.teacher.name,
            },
            "begin": self.begin.strftime('%H:%M'),
            "end": self.end.strftime('%H:%M'),
        }

        return formatted_lesson


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="teacher")


class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    lessons: Mapped[List["Lesson"]] = relationship(back_populates="group")
    faculty_id: Mapped[int] = mapped_column(ForeignKey("faculties.id"))
    faculty: Mapped["Faculty"] = relationship(back_populates="groups")


class Faculty(Base):
    __tablename__ = 'faculties'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    groups: Mapped[List["Group"]] = relationship(back_populates="faculty")

    def __str__(self):
        return f"{self.__class__.__name__} --- {self.name} ({self.id})"

    def __repr__(self):
        return str(self)
