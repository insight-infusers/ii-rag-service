import asyncio
from fastapi import APIRouter
from schema.communication import QueryEmbeddingsForSearch, TopKDocumentsResponse, Document

router = APIRouter()

@router.post("/search", response_model=TopKDocumentsResponse)
async def search_embeddings(query: QueryEmbeddingsForSearch):
    await asyncio.sleep(1)  # Simulate search processing time
    return TopKDocumentsResponse(document_ids=["doc1", "doc2", "doc3"])

@router.get("/get_text/{document_id}", response_model=Document)
async def get_document_text(document_id: str):
    # Simulate fetching document text based on document ID
    await asyncio.sleep(0.5)  # Simulate DB fetch time
    return Document(document_id=document_id, text="Simulated text content for document 1")

