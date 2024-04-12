import asyncio
import logging
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Any, AsyncGenerator
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException

logger = logging.getLogger(__name__)