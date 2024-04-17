# services/main/app/routing.py

# import asyncio
# import logging
# from fastapi import APIRouter, HTTPException
# from schema.communication import UserQueryRequest, LLMCompletionResponse
# from core.llm.llm_engine import LLMEngine
# from core.db.domain_specific_documents_db import DomainSpecificDocumentsDB
# from core.db.vector_db import VectorDBEngine
# from core.llm.embedding_engine import EmbeddingEngine

# router = APIRouter()

# @router.post("/query", response_model=LLMCompletionResponse)
# async def query_llm_endpoint(query: UserQueryRequest):
#     try:
#         # # Retrieve embedding for the query using the EmbeddingEngine
#         # # For simplification, we're assuming synchronous call to an async function
#         # query_embedding = EmbeddingEngine.embed_query(query)

#         # # Retrieve top k documents using the VectorDB
#         # top_k_document_ids = VectorDBEngine.retrieve_top_k_documents(query_embedding)

#         # # Get the completion from the LLM using the query and top k documents
#         # completion = LLMEngine.generate_completion(query.query, top_k_document_ids)

#         # Simulate retrieval and processing time
#         await asyncio.sleep(2)  # Simulates network or processing delay
#         completion = f"Processed query: {query.query}"

#         return LLMCompletionResponse(completion_text=completion)
#     except Exception as e:
#         logger.error(f"Error processing LLM query: {e}")
#         raise HTTPException(status_code=500, detail=str(e))
    
import asyncio
import logging
import httpx
from fastapi import APIRouter, HTTPException
from schema.communication import UserQueryRequest, LLMCompletionResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/query", response_model=LLMCompletionResponse)
async def query_llm_endpoint(query: UserQueryRequest):
    async with httpx.AsyncClient() as client:
        # Send user query to Retriever and get back top k document IDs
        retrieve_response = await client.post("http://retriever:8000/retrieve", json={"query": query.query})
        retrieve_data = retrieve_response.json()

        # Fetch document texts from Vector DB based on top k document IDs
        documents_texts = []
        for doc_id in retrieve_data["document_ids"]:
            text_response = await client.get(f"http://vector_db:8000/get_text/{doc_id}")
            text_data = text_response.json()
            documents_texts.append(text_data['text'])  # Access the 'text' field directly

        # Concatenate query with document texts to form the complete query
        complete_query = query.query + " " + " ".join(documents_texts)

        # Send the complete query to LLM for final processing
        llm_response = await client.post("http://llm:8000/complete", json={"query": complete_query, "document_ids": retrieve_data["document_ids"]})
        llm_data = llm_response.json()

        return LLMCompletionResponse(completion_text=llm_data["completion_text"])

