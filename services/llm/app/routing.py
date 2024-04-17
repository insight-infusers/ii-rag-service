import asyncio
from fastapi import APIRouter
from schema.communication import QueryAndDocumentsForLLM, LLMCompletionResponse

router = APIRouter()

@router.post("/complete", response_model=LLMCompletionResponse)
async def complete_query(request: QueryAndDocumentsForLLM):
    await asyncio.sleep(2)  # Simulate LLM processing time
    return LLMCompletionResponse(completion_text="Generated response for query.")
