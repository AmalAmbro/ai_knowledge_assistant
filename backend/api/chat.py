from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from rag.embeddings import embed_query
from rag.vector_store import store
from rag.prompt import build_prompt

from core.gemini_client import chat_model
from core.logging import logger
from schemas.chat import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        query = payload.query
        query_embedding = embed_query(query)

        logger.info(f"Chat query received: {query}")
        results = store.search(query_embedding)

        if not results:
            raise HTTPException(status_code=404, detail="No relevant information found")

        # Combine chunks into context for LLM
        context = "\n\n---\n\n".join(chunk for chunk, _ in results)
        prompt = build_prompt(context, query)

        # Generate answer from LLM
        response = chat_model.generate_content(prompt)
        answer = getattr(response, "text", None)
        if not answer:
            raise ValueError("LLM returned empty response")
        return ChatResponse(answer=response.text)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Chat processing failed")


# Todo

# lock this API with request size limits

# add async ingestion

# add deduplication / document IDs

# add chunk metadata (source, position)