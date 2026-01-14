from fastapi import APIRouter
from rag.chunking import chunk_text
from rag.embeddings import embed_texts
from rag.vector_store import store
from core.logging import logger
from schemas.ingest import IngestRequest, IngestResponse

router = APIRouter()

MIN_CHUNK_LEN = 30

@router.post("/ingest", response_model=IngestResponse)
def ingest_text(payload: IngestRequest):
    try:
        print(f"Text: {payload.text}")
        chunks = chunk_text(payload.text)
        original_count = len(chunks)
        chunks = [c for c in chunks if len(c.strip()) >= MIN_CHUNK_LEN]
        filtered_count = original_count - len(chunks)

        if not chunks:
            logger.info(f"Ingested text: 0 chunks added (filtered out {filtered_count})")
            return IngestResponse(chunks_added=0)

        embeddings = embed_texts(chunks)
        store.add(embeddings, chunks)
        logger.info(f"Ingested text: {len(chunks)} chunks added (filtered out {filtered_count})")

        return IngestResponse(chunks_added=len(chunks))
    except Exception as e:
        return IngestResponse(chunks_added=0, error=str(e))
