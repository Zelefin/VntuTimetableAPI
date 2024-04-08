from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.groups import group_router
from app.routes.faculties import faculty_router


app = FastAPI()
app.include_router(router=group_router)
app.include_router(router=faculty_router)

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
