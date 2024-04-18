import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.logging_cfg import InterceptHandler
from app.routes.groups import group_router
from app.routes.faculties import faculty_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.info("App started!")
    yield
    logging.info("App stopped!")


app = FastAPI(lifespan=lifespan)
app.include_router(router=group_router)
app.include_router(router=faculty_router)
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
    return {"message": "Hello World"}
