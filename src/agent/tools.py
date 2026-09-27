from typing import Any
from schemas import AddToolArgs, WeatherToolArgs
import asyncio
import inspect


def get_weather(city: str, days: int = 1) -> str:
    return f"{city} 未来 {days} 天天气：晴，25°C"


def add(a: int, b: int) -> int:
    return a + b

ARG_MODELS = {
    "get_weather": WeatherToolArgs,
    "add": AddToolArgs,
}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市未来若干天的天气",
            "parameters": WeatherToolArgs.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "计算两个整数的和",
            "parameters": AddToolArgs.model_json_schema(),
        },
    },
]

TOOLS = {
    "get_weather": get_weather,
    "add": add,
}


async def execute_tool(
    tool_name: str, 
    arguments: dict,
    timeout: float = 10.0,
    max_retries: int = 2,
    ) -> Any:
    tool = TOOLS.get(tool_name)

    if tool is None:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

    for attempt in range(max_retries + 1):
        try:
            if inspect.iscoroutinefunction(tool):
                task = tool(**arguments)
            else:
                task = asyncio.to_thread(
                    tool,
                    **arguments,
                )

            return await asyncio.wait_for(
                task,
                timeout=timeout,
            )

        except (TimeoutError, ConnectionError):
            if attempt == max_retries:
                raise

            await asyncio.sleep(1)

    # if inspect.iscoroutinefunction(tool):
    #     task = tool(**arguments)
    # else:
    #     task = asyncio.to_thread(
    #         tool,
    #         **arguments,
    #     )

    # return await asyncio.wait_for(
    #     task,
    #     timeout=timeout,
    # )