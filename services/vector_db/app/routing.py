import asyncio
from fastapi import APIRouter, HTTPException
from schema.communication import QueryEmbeddingsForSearch, TopKDocumentsResponse, Document


router = APIRouter()

