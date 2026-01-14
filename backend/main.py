from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

from core.logging import logger
from core.exceptions import LLMError, VectorStoreError


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.exception_handler(LLMError)
async def llm_error_handler(request: Request, exc: LLMError):
    logger.error("LLM failure: %s", exc)
    return JSONResponse(
        status_code=503,
        content={"answer": "LLM is temporarily unavailable"}
    )

@app.exception_handler(VectorStoreError)
async def vector_store_error_handler(request: Request, exc: VectorStoreError):
    logger.error("Vector store failure: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"answer": "Knowledge base error"}
    )

from api.ingest import router as ingest_router
from api.chat import router as chat_router

app.include_router(ingest_router)
app.include_router(chat_router)
