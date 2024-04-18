# services/main/app/routing.py

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
        request_json = {"query": query.query}
        logger.info(f'Sending request to retriever {request_json}')
        retrieve_response = await client.post("http://retriever:8000/retrieve", json=request_json)
        retrieve_data = retrieve_response.json()
        logger.info(f'Received response from retriever {retrieve_data}')

        # Fetch document texts from Vector DB based on top k document IDs
        documents_texts = []
        for doc_id in retrieve_data["document_ids"]:
            logger.info(f'Sending request to vector database')
            text_response = await client.get(f"http://vector_db:8000/get_text/{doc_id}")
            text_data = text_response.json()
            documents_texts.append(text_data['text'])  # Access the 'text' field directly
            logger.info(f'Received response from vector database')

        # Concatenate query with document texts to form the complete query
        complete_query = query.query + " " + " ".join(documents_texts)

        # Send the complete query to LLM for final processing
        logger.info(f'Sending request to LLM engine')
        llm_response = await client.post("http://llm:8000/complete", json={"query": complete_query, "document_ids": retrieve_data["document_ids"]})
        llm_data = llm_response.json()
        logger.info(f'Received response from LLM engine')

        return LLMCompletionResponse(completion_text=llm_data["completion_text"])

