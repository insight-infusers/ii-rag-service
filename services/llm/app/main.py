# services/main/app/main.py

import logging
from fastapi import FastAPI
from app.routing import router
from config import settings
from core.utils.logging import setup_logging

# Initialize the logger
setup_logging(level=logging.DEBUG if settings.verbose else logging.INFO)

# Create FastAPI app instance
app = FastAPI(title=settings.title, version=settings.version)

# Include the routers from the routing module
app.include_router(router)

# Lifespan events for startup and shutdown can be added if necessary
@app.on_event("startup")
async def startup_event():
    logging.getLogger(__name__).info("Starting up the Main RAG Service...")

@app.on_event("shutdown")
async def shutdown_event():
    logging.getLogger(__name__).info("Shutting down the Main RAG Service...")