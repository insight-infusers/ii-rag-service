# communication.py
# JSON schema for API communication between RAG service components using FastAPI and Pydantic

from pydantic import BaseModel, FilePath
from typing import Union, List

class DocToEmbedRequest(BaseModel):
    """DomainSpecificDocuments → Embedder:
    Embedder receives new documents to process either as direct text or file path."""
    document_id: str
    document_text_or_path: Union[str, FilePath]

class DocEmbedding(BaseModel):
    """Embedder → VectorDB OR Embedder → Retriever:
    Embedder sends the embeddings to be indexed and stored in VectorDB OR retrieved by Retriever."""
    document_id: str
    embedding: List[float]  # suitable type for embeddings

class Document(BaseModel):
    """VectorDB → User:
    VectorDB sends the retrieved document texts to the User."""
    document_id: str
    text: str

class UserQueryRequest(BaseModel):
    """User → Retriever:
    User sends a query to the Retriever for searching top relevant documents."""
    query: str

class QueryToEmbedRequest(BaseModel):
    """Retriever → Embedder:
    Retriever sends a query to the Embedder to get the query embeddings."""
    query: str

class QueryEmbedding(BaseModel):
    """Embedder → Retriever:
    Embedder returns embeddings back to Retriever."""
    query: str
    embedding: List[float]

class QueryEmbeddingsForSearch(BaseModel):
    """Retriever → VectorDB:
    Retriever sends embedded query to VectorDB to fetch top k documents."""
    query_embedding: List[float]

class TopKDocumentsResponse(BaseModel):
    """VectorDB → Retriever:
    VectorDB returns top k relevant documents to Retriever."""
    document_ids: List[str]  # top k document IDs

class QueryAndDocumentsForLLM(BaseModel):
    """Retriever → LLM:
    Retriever sends the original query along with top k documents to LLM."""
    query: str
    document_ids: List[str]

class LLMCompletionResponse(BaseModel):
    """LLM → User:
    LLM returns the completion response back to the User."""
    completion_text: str