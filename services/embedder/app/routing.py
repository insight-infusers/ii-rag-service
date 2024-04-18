import asyncio
import httpx
import logging
from fastapi import APIRouter
from schema.communication import DocToEmbedRequest, DocEmbedding, QueryToEmbedRequest

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/embed", response_model=DocEmbedding)
async def embed_document(doc_request: DocToEmbedRequest):
    # logger.info(f'Extracting document text')
    # document_text = ""
    # if isinstance(doc_request.document_text_or_path, str):
    #     document_text = doc_request.document_text_or_path
    # else:
    #     # Assuming it's a path to a file, read the content
    #     with open(doc_request.document_text_or_path, 'r') as file:
    #         document_text = file.read()
    # logger.info(f'Extracted document text')

    logger.info(f'Extracting embedding from text')
    await asyncio.sleep(1)  # Simulate embedding processing time
    # Dummy embedding generation
    embedding = [0.1, 0.2, 0.3]  # Ideally, call a real ML model here
    logger.info(f'Embedding extracted')

    return DocEmbedding(document_id=doc_request.document_id, embedding=embedding)

