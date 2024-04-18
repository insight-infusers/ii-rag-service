import asyncio
import logging
from fastapi import FastAPI
from app.routing import router
from config import settings

from core.llm.llm_engine import OpenAILLMEngine
from schema.communication import LLMCompletionResponse, QueryAndDocumentsForLLM


app = FastAPI(title=settings.title, version=settings.version)
app.include_router(router)
logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup_event():
    app.llm_engine = OpenAILLMEngine(
        api_key=settings.OPENAI_API_KEY,
        model=settings.LLM_MODEL,
        )
    logger.info("LLM Engine initialized")
    logger.info("Starting up, registering routes...")
    logger.info(app.routes)

@app.post("/complete", response_model=LLMCompletionResponse)
async def complete_query(request: QueryAndDocumentsForLLM):
    # await asyncio.sleep(2)  # Simulate LLM processing time
    completion_text = await app.llm_engine.query(text=request.query)
    return LLMCompletionResponse(completion_text=completion_text)