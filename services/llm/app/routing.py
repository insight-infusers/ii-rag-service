import asyncio
from fastapi import APIRouter
from schema.communication import QueryAndDocumentsForLLM, LLMCompletionResponse

router = APIRouter()
