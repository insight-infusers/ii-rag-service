import asyncio
import httpx
from fastapi import APIRouter
from schema.communication import QueryToEmbedRequest, QueryEmbeddingsForSearch, TopKDocumentsResponse

router = APIRouter()

@router.post("/retrieve", response_model=TopKDocumentsResponse)
async def retrieve_documents(query: QueryToEmbedRequest):
    async with httpx.AsyncClient() as client:
        # Simulate embedding request to Embedder and fetch embeddings
        embed_response = await client.post("http://embedder:8000/embed", json={"query": query.query})
        embed_data = embed_response.json()

        # Send embedding to Vector DB for searching top k documents
        search_response = await client.post("http://vector_db:8000/search", json={"query_embedding": embed_data["embedding"]})
        search_data = search_response.json()
        return TopKDocumentsResponse(document_ids=search_data["document_ids"])

