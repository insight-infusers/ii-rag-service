from abc import ABC, abstractmethod
import lancedb
from sentence_transformers import SentenceTransformer, CrossEncoder
import torch
import asyncio

class VectorDBEngine(ABC):
    @abstractmethod
    def __init__(self, db_location):
        pass

    @abstractmethod
    async def add_document(self, doc_id: str, text: str):
        pass

    @abstractmethod
    async def search(self, query: str, top_k: int):
        pass

    @abstractmethod
    async def rerank(self, query: str, search_results, top_k: int):
        pass

class LanceDBEngine(VectorDBEngine):
    def __init__(self, db_location, table_name, embedder_model, reranker_model):
        self.db = lancedb.connect(db_location)
        self.table = self.db.open_table(table_name)
        self.query_model = SentenceTransformer(embedder_model, device="cpu")
        self.reranker_model = CrossEncoder(reranker_model, device="cpu")

    async def add_document(self, doc_id, text):
        vector = self.query_model.encode(text, convert_to_numpy=True)
        self.table.insert({"_id": doc_id, "text": text, "vector": vector})
        await asyncio.sleep(0)  # simulate async behavior

    async def search(self, query, top_k=20):
        query_vector = self.query_model.encode(query, convert_to_numpy=True)
        search_results = self.table.search(query_vector).limit(top_k)
        return search_results.to_pandas()

    async def rerank(self, query, search_results, top_k=5):
        query_retrieve_comb = [[query, sent] for sent in search_results["text"]]
        scores = self.reranker_model.predict(query_retrieve_comb, activation_fct=torch.nn.Sigmoid())
        search_results['_distance_reranked'] = scores
        topk = search_results.sort_values('_distance_reranked', ascending=False).head(top_k)
        return topk

# Usage example:
async def main(**settings):
    db_engine = LanceDBEngine(
        db_location=settings.get("VECTOR_DB_PATH"),
        table_name=settings.get("VECTOR_DB_TABLE_NAME", "all-mpnet-base-v2_384.lance")
        embedder_model=settings.get("EMBEDDING_MODEL", "all-mpnet-base-v2"),
        reranker_model=settings.get("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
    )

    # Adding a document
    await db_engine.add_document(doc_id="1", text="Example text about AI in healthcare")

    # Searching
    search_results = await db_engine.search("AI and healthcare", top_k=10)
    print(search_results)

    # Re-ranking
    reranked_results = await db_engine.rerank("AI and healthcare", search_results)
    print(reranked_results)

if __name__ == "__main__":
    import asyncio
    import config
    settings = config.settings
    asyncio.run(main(**settings))
