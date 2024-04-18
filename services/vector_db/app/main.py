import asyncio
from fastapi import FastAPI, HTTPException
from .routing import router
from config import settings
from core.db.vector_db import LanceDBEngine
import logging

from schema.communication import QueryEmbeddingsForSearch, TopKDocumentsResponse, Document

app = FastAPI(title=settings.title, version=settings.version)
app.include_router(router)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Assuming that settings have all the necessary configuration values
    app.vector_db_engine = LanceDBEngine(
        db_location=settings.VECTOR_DB_PATH,
        table_name=settings.VECTOR_DB_TABLE_NAME,
        embedder_model=settings.EMBEDDER_MODEL,
        reranker_model=settings.RERANKER_MODEL
    )
    logger.info("Vector DB Engine initialized")
    logger.info("Starting up, registering routes...")
    logger.info(app.routes)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the Vector DB service")

@app.post("/search", response_model=TopKDocumentsResponse)
async def search_embeddings(query: QueryEmbeddingsForSearch):
    try:
        search_results = await app.db_engine.search(query.query, top_k=10)
        document_ids = ["" for doc in search_results.to_dict('text')]
        return TopKDocumentsResponse(document_ids=document_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_text/{document_id}", response_model=Document)
async def get_document_text(document_id: str):
    try:
        # Here we should ideally fetch the actual document content from the LanceDB
        # For now, simulate fetching
        await asyncio.sleep(0.5)  # Simulate DB fetch time
        text = f"Simulated text content for document {document_id}"
        return Document(document_id=document_id, text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
