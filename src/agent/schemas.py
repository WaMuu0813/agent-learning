from pydantic import BaseModel
from typing import Literal


class WeatherToolArgs(BaseModel):
    city: str
    days: int = 1

class AddToolArgs(BaseModel):
    a: int
    b: int

class SearchWebArgs(BaseModel):
    query: str


class SearchWebToolCall(BaseModel):
    name: Literal["search_web"]
    arguments: SearchWebArgs

class WeatherToolCall(BaseModel):
    name: Literal["get_weather"]
    arguments: WeatherToolArgs


class AddToolCall(BaseModel):
    name: Literal["add"]
    arguments: AddToolArgs

ToolCall = WeatherToolCall | AddToolCall | SearchWebToolCall


# class ToolCall(BaseModel):
#     name: str
#     arguments: WeatherToolArgs


class AgentResponse(BaseModel):
    thought: str
    tool_call: ToolCall | None = None
    final_answer: str | None = None