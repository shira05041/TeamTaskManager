from fastapi import FastAPI
from app.routers import auth
from app.schemas import project, team, user, task, comment
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["auth"])
