import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request

from rag_pipeline import RAGService
from rag_schemas import (
    ChatRequest,
    ChatResponse,
    Source,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("正在启动 RAG 服务")

    app.state.rag_service = RAGService()

    logger.info("RAG 服务启动完成")

    yield

    logger.info("RAG 服务正在关闭")


app = FastAPI(
    title="Local Knowledge Base RAG",
    lifespan=lifespan,
)


@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    http_request: Request,
):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="message 不能为空",
        )

    rag_service = http_request.app.state.rag_service

    try:
        answer, documents = await rag_service.ask(
            request.message
        )

    except Exception:
        logger.exception(
            "RAG request failed"
        )

        raise HTTPException(
            status_code=502,
            detail="RAG 服务调用失败",
        )

    sources = []

    for doc in documents:
        metadata = doc.metadata

        section = (
            metadata.get("h3")
            or metadata.get("h2")
            or metadata.get("h1")
        )

        sources.append(
            Source(
                source=metadata.get(
                    "source",
                    "unknown",
                ),
                page=metadata.get("page"),
                section=section,
                content=doc.page_content[:300],
            )
        )

    return ChatResponse(
        answer=answer,
        sources=sources,
    )