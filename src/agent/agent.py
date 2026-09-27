from llm import call_llm
from tools import ARG_MODELS, execute_tool
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


async def run_agent(user_input: str, max_steps: int = 5) -> str:

    messages = [
        {
            "role": "system",
            "content": "你是一个有帮助的助手。需要工具时请选择合适的工具。",
        },
        {
            "role": "user",
            "content": user_input,
        },
    ]

    for step in range(max_steps):
        logger.info(
            "Agent step: %s",
            step + 1,
        )

        response = await call_llm(messages)

        message = response.choices[0].message

        # 模型不再调用工具，说明已经得到最终答案
        if not message.tool_calls:
            return message.content or ""

        # 把模型这一次的 Tool Call 记录到对话历史
        messages.append(message.model_dump(exclude_none=True))

        # 模型一次可能提出多个 Tool Call
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            raw_arguments = tool_call.function.arguments

            # print(f"\n[Tool Call] {tool_name}")
            # print("[Raw Arguments]", raw_arguments)

            logger.info(
                "Tool call: %s",
                tool_name,
            )

            arg_model = ARG_MODELS.get(tool_name)

            if arg_model is None:
                raise ValueError(f"Unknown tool: {tool_name}")
            try:
                validated_args = arg_model.model_validate_json(raw_arguments)

                arguments = validated_args.model_dump()

                try:
                    result = await execute_tool(
                        tool_name=tool_name,
                        arguments=arguments,
                    )
                    logger.info(
                        "Tool result: %s",
                        result,
                    )
                except Exception as e:
                    logger.exception("Tool execution failed")
                    result = f"Tool execution failed: {e}"
                    # print("[Tool Result]", result)

            except Exception as e:
                result = f"Tool execution failed: {e}"

            # 把工具执行结果重新告诉 LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    raise RuntimeError(f"Agent exceeded max_steps={max_steps}")
