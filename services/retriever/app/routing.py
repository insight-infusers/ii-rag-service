import asyncio
import logging
import httpx
from fastapi import APIRouter
from schema.communication import QueryToEmbedRequest, TopKDocumentsResponse

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/retrieve", response_model=TopKDocumentsResponse)
async def retrieve_documents(query: QueryToEmbedRequest):
    async with httpx.AsyncClient() as client:
        # Simulate embedding request to Embedder and fetch embeddings
        request_json = dict(document_id="234", document_text_or_path=query.dict()["query"])
        logger.info(f'Sending request to Embedder')
        embed_response = await client.post("http://embedder:8000/embed", json=request_json)
        embed_data = embed_response.json()
        logger.info(f'Received response from Embedder')

        # Send embedding to Vector DB for searching top k documents
        logger.info(f'Sending request to vector database')
        search_response = await client.post("http://vector_db:8000/search", json={"query_embedding": embed_data["embedding"]})
        search_data = search_response.json()
        logger.info(f'Received response from vector database')
        return TopKDocumentsResponse(document_ids=search_data["document_ids"])

