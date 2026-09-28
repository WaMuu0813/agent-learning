from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


class Source(BaseModel):
    source: str
    page: int | None = None
    section: str | None = None
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]