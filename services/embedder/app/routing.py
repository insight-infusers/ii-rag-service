import asyncio
from fastapi import APIRouter
from schema.communication import DocToEmbedRequest, DocEmbedding

router = APIRouter()

@router.post("/embed", response_model=DocEmbedding)
async def embed_document(doc_request: DocToEmbedRequest):
    await asyncio.sleep(1)  # Simulate embedding processing time
    return DocEmbedding(document_id=doc_request.document_id, embedding=[0.1, 0.2, 0.3])
