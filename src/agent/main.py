# # from schemas import AgentResponse, ToolCall


# # tool_call = ToolCall(
# #     name="get_weather",
# #     arguments={
# #         "city": "Hefei"
# #     }
# # )

# # response = AgentResponse(
# #     thought="用户正在询问天气，我需要调用天气工具。",
# #     tool_call=tool_call
# # )

# # print(response)

# # print("tool name:", response.tool_call.name)
# # print("arguments:", response.tool_call.arguments)

# # llm_output = """
# # {
# #     "thought": "用户想查询合肥未来三天天气",
# #     "tool_call": {
# #         "name": "get_weather",
# #         "arguments": {
# #             "city": "Hefei",
# #             "days": 3
# #         }
# #     },
# #     "final_answer": null
# # }
# # """

# from re import search
# from unittest import result
# from schemas import AgentResponse
# from llm import ask_llm



# def get_weather(city: str, days: int = 1) -> str:
#     return f"{city} 未来 {days} 天天气：晴，25°C"

# def add(a: int,b: int) -> int:
#     return a + b

# def search_web(query: str) -> str:
#     return 0

# TOOLS = {
#     "get_weather": get_weather,
#     "add": add,
#     "search_web": search_web
# }


# llm_output = """
# {
#     "thought": "用户想查询天气",
#     "tool_call": {
#         "name": "get_weather",
#         "arguments": {
#             "city": "Hefei",
#             "days": 3
#         }
#     },
#     "final_answer": null
# }
# """


# # response = AgentResponse.model_validate_json(llm_output)
# response = ask_llm("帮我查询合肥未来三天天气")

# print(response)
# print(type(response))

# if response.tool_call is not None:
#     print("tool:", response.tool_call.name)
#     print("arguments:", response.tool_call.arguments)
# else:
#     print("final answer:", response.final_answer)

# # print("Agent 思考：", response.thought)

# # if response.tool_call is not None:
# #     tool_name = response.tool_call.name
# #     # args = response.tool_call.arguments
# #     args_dict = response.tool_call.arguments.model_dump()

# #     tool = TOOLS.get(tool_name)
# #     if tool is None:
# #         raise ValueError(f"Unknown tool: {tool_name}")

# #     result = tool(**args_dict)
# #     # result = tool(
# #     #     city=args.city,
# #     #     days=args.days
# #     # )

# #     print("Tool result:", result)
# #     print("Arguments:", args_dict)
# #     print("Tool result:", result)
# #     # if tool_name == "get_weather":
# #     #     result = get_weather(
# #     #         city=args.city,
# #     #         days=args.days
# #     #     )

# #     #     print("Tool result:", result)

# from llm import ask_llm
# from tools import execute_tool
# from tools import ARG_MODELS

# user_input = input("You: ") 

# message = ask_llm(user_input)

# if not message.tool_calls:
#     print("Agent:", message.content)

# else:
#     for tool_call in message.tool_calls:
#         tool_name = tool_call.function.name
#         raw_arguments = tool_call.function.arguments
 
#         print("Tool:", tool_name)
#         print("Raw arguments:", raw_arguments)

#         arg_model = ARG_MODELS.get(tool_name)

#         if arg_model is None:
#             raise ValueError(f"Unknown tool: {tool_name}")

#         validated_args = arg_model.model_validate_json(
#             raw_arguments
#         )

#         arguments = validated_args.model_dump()

#         print("Validated arguments:", arguments)

#         result = execute_tool(
#             tool_name=tool_name,
#             arguments=arguments,
#         )

#         print("Tool result:", result)

# response = ask_llm(user_input)

# print("\nAgent thought:", response.thought)


# if response.tool_call is not None:
#     tool_name = response.tool_call.name
#     arguments = response.tool_call.arguments.model_dump()

#     print("Tool:", tool_name)
#     print("Arguments:", arguments)

#     result = execute_tool(
#         tool_name=tool_name,
#         arguments=arguments,
#     )

#     print("Tool result:", result)

# else:
#     print("Agent:", response.final_answer)

from agent import run_agent


user_input = input("You: ")

answer = run_agent(user_input)

print("\nAgent:", answer)