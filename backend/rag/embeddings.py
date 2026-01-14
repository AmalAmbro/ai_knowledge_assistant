import google.generativeai as genai
from core.gemini_client import embedding_model


def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Used for document ingestion (batch)
    """
    response = genai.embed_content(
        model=embedding_model,
        content=texts,
        task_type="retrieval_document"
    )

    return response["embedding"]


def embed_query(query: str) -> list[float]:
    """
    Used for search queries (single)
    """
    response = genai.embed_content(
        model=embedding_model,
        content=query,
        task_type="retrieval_query"
    )

    return response["embedding"]
