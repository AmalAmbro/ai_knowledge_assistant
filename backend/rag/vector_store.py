from asyncio.log import logger
import faiss
import numpy as np
import os
import pickle
from typing import List, Tuple
from core.logging import logger


EMBEDDING_DIM = 768  # Gemini text-embedding-004 dimension
SIMILARITY_THRESHOLD = 0.7

class FAISSStore:
    def __init__(self, dim: int, persist_dir: str = "storage"):
        self.dim = dim
        self.persist_dir = persist_dir
        self.index_path = os.path.join(persist_dir, "faiss.index")
        self.texts_path = os.path.join(persist_dir, "texts.pkl")

        os.makedirs(persist_dir, exist_ok=True)

        self.index = None
        self.texts: List[str] = []

        self._load()

    def _load(self):
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            logger.info("Loaded FAISS index with %d vectors", self.index.ntotal)
        else:
            self.index = faiss.IndexFlatIP(self.dim)
            logger.info("New FAISS IP index created")

        if os.path.exists(self.texts_path):
            with open(self.texts_path, "rb") as f:
                self.texts = pickle.load(f)
        else:
            self.texts = []

    def _persist(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.texts_path, "wb") as f:
            pickle.dump(self.texts, f)

    def add(self, embeddings: List[List[float]], texts: List[str]):
        vectors = np.array(embeddings).astype("float32")
        vectors = self._normalize(vectors)

        self.index.add(vectors)
        self.texts.extend(texts)
        self._persist()
        logger.info(f"Added {len(texts)} chunks to FAISS")

    def search(
        self,
        query_embedding,
        top_k=5,
        min_score=0.45
    ):
        if self.index.ntotal == 0:
            return []

        top_k = min(top_k, self.index.ntotal)

        query_vector = np.array([query_embedding]).astype("float32")
        query_vector = self._normalize(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
            if idx == -1:
                continue

            if score >= min_score:
                logger.info(
                    f"Rank={rank+1} | Score={score:.4f} | Chunk='{self.texts[idx][:80]}'"
                )
                results.append((self.texts[idx], float(score)))

        if not results:
            logger.info(f"NO MATCHES above min_score={min_score}")
        
        return results

    @staticmethod
    def _normalize(vectors: np.ndarray):
        return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)


store = FAISSStore(dim=EMBEDDING_DIM)
