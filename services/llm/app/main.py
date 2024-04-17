from fastapi import FastAPI
from app.routing import router
from config import settings

app = FastAPI(title=settings.title, version=settings.version)
app.include_router(router)
