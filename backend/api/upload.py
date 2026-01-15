from fastapi import APIRouter, UploadFile, File
from services.fileparser import extract_text_from_file
from rag.chunking import chunk_text
from rag.embeddings import embed_texts
from rag.vector_store import store
from pathlib import Path


router = APIRouter()

MIN_CHUNK_LEN = 200

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    safe_name = Path(file.filename).stem
    text = extract_text_from_file(file)

    import os
    os.makedirs("uploads", exist_ok=True)

    with open(f"uploads/{safe_name}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    chunks = chunk_text(text)
    chunks = [c for c in chunks if len(c.strip()) >= MIN_CHUNK_LEN]

    if not chunks:
        return {"chunks_added": 0}

    embeddings = embed_texts(chunks)
    store.add(embeddings, chunks)

    return {"chunks_added": len(chunks)}
