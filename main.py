import logging
from datetime import datetime

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.logging_cfg import InterceptHandler
from app.routes.groups import group_router
from app.routes.faculties import faculty_router
from app.routes.teachers import teachers_router
from app.scheduled_tasks import (
    update_faculties_table,
    update_groups_table,
    update_groups_lessons_table,
)
from configreader import Config, load_config
from db.db import sa_sessionmaker


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info("App started!")

    config: Config = load_config()
    session_maker = sa_sessionmaker(config.postgres)

    scheduler = AsyncIOScheduler(timezone="Europe/Kyiv")
    scheduler.start()

    retry_faculties: Job = scheduler.add_job(
        update_faculties_table,
        trigger="interval",
        minutes=10,
        start_date=datetime.now(),
        kwargs={
            "session_factory": session_maker,
            "retry_task": None,
        },
    )
    retry_faculties.kwargs["retry_task"] = retry_faculties
    retry_faculties.pause()

    retry_groups: Job = scheduler.add_job(
        update_groups_table,
        trigger="interval",
        minutes=10,
        start_date=datetime.now(),
        kwargs={
            "session_factory": session_maker,
            "retry_task": None,
        },
    )
    retry_faculties.kwargs["retry_task"] = retry_groups
    retry_groups.pause()

    # retry_teachers: Job = ...
    # retry_teachers.kwargs["retry_task"] = retry_teachers
    # retry_teachers.pause()

    retry_groups_lessons: Job = scheduler.add_job(
        update_groups_lessons_table,
        trigger="interval",
        minutes=10,
        start_date=datetime.now(),
        kwargs={
            "session_factory": session_maker,
            "retry_task": None,
        },
    )
    retry_groups_lessons.kwargs["retry_task"] = retry_groups_lessons
    retry_groups_lessons.pause()

    # Main tasks

    scheduler.add_job(
        update_faculties_table,
        trigger="cron",
        day=1,
        start_date=datetime.now(),
        kwargs={
            "session_factory": session_maker,
            "retry_task": retry_faculties,
        },
    )
    scheduler.add_job(
        update_groups_table,
        trigger="cron",
        day=1,
        hour=1,
        start_date=datetime.now(),
        kwargs={
            "session_factory": session_maker,
            "retry_task": retry_groups,
        },
    )
    # Because by updating groups lessons table we also update teachers table
    # so, we don't really need this scheduled job
    # scheduler.add_job(
    #     update_teachers_table, trigger='cron', hour=3, minute=0, start_date=datetime.now(),
    #     kwargs={"session_factory": sa_sessionmaker(config.postgres), "retry_task": retry_teachers},
    # )
    scheduler.add_job(
        update_groups_lessons_table,
        trigger="cron",
        hour=5,
        start_date=datetime.now(),
        kwargs={
            "session_factory": session_maker,
            "retry_task": retry_groups_lessons,
        },
    )
    yield
    scheduler.shutdown()
    logging.info("App stopped!")


app = FastAPI(lifespan=lifespan)
app.include_router(router=group_router)
app.include_router(router=faculty_router)
app.include_router(router=teachers_router)
# For handling errors
logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to VNTU timetable API"}
