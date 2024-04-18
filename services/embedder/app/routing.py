import asyncio
from fastapi import APIRouter, HTTPException, UploadFile, File
from schema.communication import DocToEmbedRequest, DocEmbedding
import os

router = APIRouter()

@router.post("/embed", response_model=DocEmbedding)
async def embed_document(doc_request: DocToEmbedRequest):
    try:
        document_text = ""
        if isinstance(doc_request.document_text_or_path, str):
            document_text = doc_request.document_text_or_path
        else:
            # Assuming it's a file, read the content
            with open(doc_request.document_text_or_path, 'r') as file:
                document_text = file.read()

        await asyncio.sleep(1)  # Simulate embedding processing time
        # Dummy embedding generation
        embedding = [0.1, 0.2, 0.3]  # Ideally, call a real ML model here

        return DocEmbedding(document_id=doc_request.document_id, embedding=embedding)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

