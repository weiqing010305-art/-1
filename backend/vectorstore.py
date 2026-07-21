import chromadb

from backend.config import Config
from backend.embeddings import Embedder


class VectorStore:
    """Chroma 持久化向量库的轻封装。"""

    def __init__(self, path: str, embedder: Embedder):
        self.client = chromadb.PersistentClient(path=path)
        self.embedder = embedder
        self.collection = None

    def create_or_get(self, name: str):
        self.collection = self.client.get_or_create_collection(name=name)

    def add(self, chunks: list[dict], doc_id: str):
        if not chunks:
            return
        texts = [c["text"] for c in chunks]
        embeddings = self.embedder.embed(texts)
        ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
        metadatas = [{"page": c["page"], "doc_id": doc_id} for c in chunks]
        self.collection.add(
            ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas
        )

    def query(self, question: str, top_k: int = 4, where: dict | None = None):
        emb = self.embedder.embed([question])[0]
        return self.collection.query(
            query_embeddings=[emb], n_results=top_k, where=where
        )
