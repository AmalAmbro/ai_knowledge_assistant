from pydantic import BaseModel

class IngestRequest(BaseModel):
    text: str

class IngestResponse(BaseModel):
    chunks_added: int
    error: str | None = None
