# services/main/app/routing.py

import logging
from fastapi import APIRouter, HTTPException
from schema.communication import UserQueryRequest, LLMCompletionResponse
from core.llm.llm_engine import LLMEngine
from core.db.domain_specific_documents_db import DomainSpecificDocumentsDB
from core.db.vector_db import VectorDBEngine
from core.llm.embedding_engine import EmbeddingEngine

# Set up logging for the service
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/query", response_model=LLMCompletionResponse)
async def query_llm_endpoint(query: UserQueryRequest):
    try:
        # Retrieve embedding for the query using the EmbeddingEngine
        # For simplification, we're assuming synchronous call to an async function
        query_embedding = EmbeddingEngine.embed_query(query)

        # Retrieve top k documents using the VectorDB
        top_k_document_ids = VectorDBEngine.retrieve_top_k_documents(query_embedding)

        # Get the completion from the LLM using the query and top k documents
        completion = LLMEngine.generate_completion(query.query, top_k_document_ids)

        return LLMCompletionResponse(completion_text=completion)
    except Exception as e:
        logger.error(f"Error processing LLM query: {e}")
        raise HTTPException(status_code=500, detail=str(e))