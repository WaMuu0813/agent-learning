# import os

# from dotenv import load_dotenv
# from openai import OpenAI

# from schemas import AgentResponse


# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     base_url="https://api.deepseek.com",
# )


# def ask_llm(user_input: str) -> AgentResponse:
#     response = client.chat.completions.create(
#         model="deepseek-flash",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """
# 你是一个 Agent。

# 你必须输出 JSON。

# 输出格式如下：

# {
#     "thought": "你的判断",
#     "tool_call": {
#         "name": "get_weather",
#         "arguments": {
#             "city": "Hefei",
#             "days": 3
#         }
#     },
#     "final_answer": null
# }

# 规则：
# 1. 如果用户需要查询天气，使用 get_weather。
# 2. 如果用户要求两个整数相加，使用 add。
# 3. 如果不需要工具，tool_call 为 null，并填写 final_answer。
# """,
#             },
#             {
#                 "role": "user",
#                 "content": user_input,
#             },
#         ],
#         response_format={
#             "type": "json_object"
#         },
#     )

#     content = response.choices[0].message.content

#     return AgentResponse.model_validate_json(content)

import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import TOOL_DEFINITIONS

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY is not set")


client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)


def ask_llm(user_input: str):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": "你是一个有帮助的助手。需要工具时请选择合适的工具。",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
        extra_body={"thinking": {"type": "disabled"}},
    )

    return response.choices[0].message
