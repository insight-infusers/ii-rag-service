import asyncio
import logging
from fastapi import FastAPI
from app.routing import router
from config import settings

# Import the embedding engine
from core.llm.embedding_engine import OpenAIEmbeddingEngine
from schema.communication import EmbeddingResponse, DocToEmbedRequest

app = FastAPI(title=settings.title, version=settings.version)
app.include_router(router)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Initialize the embedding engine with the API key and model settings from config
    app.embedding_engine = OpenAIEmbeddingEngine(
        api_key=settings.OPENAI_API_KEY,
        model=settings.EMBEDDING_MODEL  # Ensure this setting exists in your config
    )
    logger.info("Embedding engine initialized")
    logger.info("Starting up, registering routes...")
    logger.info(app.routes)

@app.post("/embed", response_model=EmbeddingResponse)
async def get_embedding(request: DocToEmbedRequest):
    # Fetch the embedding for the text provided in the request
    embedding = await app.embedding_engine.get_embedding(request.document_text)
    return EmbeddingResponse(document_id=request.document_id, embedding=embedding)
