import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import run_agent

logger = logging.getLogger(__name__)

app = FastAPI()

users = {
    1: "Tom",
    2: "Jack",
}


class TaskRequest(BaseModel):
    message: str
    priority: int = 1


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
def root():
    return {"message": "Agent service is running"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="message cannot be empty",
        )
    try:
        answer = await run_agent(request.message)
        return ChatResponse(answer=answer)

    except Exception:
        logger.exception("Agent execution failed")
        raise HTTPException(
            status_code=502,
            detail="LLM service failed",
        )


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="user not found",
        )
    return {
        "user_id": user_id,
        "name": users[user_id],
    }


@app.post("/users/{user_id}/tasks")
def create_task(
    user_id: int,
    notify: bool = False,
    task: TaskRequest | None = None,
):
    return {
        "user_id": user_id,
        "notify": notify,
        "task": task,
    }
