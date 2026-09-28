import asyncio
import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_text_splitters import RecursiveCharacterTextSplitter


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


format_docs_runnable = RunnableLambda(format_docs)

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY is not set")


model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=api_key,
    temperature=0,
)

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "你是一个简洁、准确的 AI 助手。"
#         ),
#         (
#             "human",
#             "请解释这个概念：{topic}"
#         ),
#     ]
# )

parser = StrOutputParser()

# chain = prompt | model | parser

short_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个简洁的助手。"),
        ("human", "用一句话解释：{topic}"),
    ]
)

detailed_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个技术老师。"),
        ("human", "详细解释：{topic}"),
    ]
)

short_chain = short_prompt | model | parser
detailed_chain = detailed_prompt | model | parser

parallel = RunnableParallel(
    short=short_chain,
    detailed=detailed_chain,
)


async def main():
    text = """
        Agent 是能够根据目标自主决定下一步操作的系统。

        Tool Calling 允许模型选择并调用外部工具，例如搜索、数据库和 API。

        RAG 会先从知识库检索相关资料，再把资料交给模型生成答案。

        Redis 是常见的内存数据库，可以用于缓存、会话状态和任务状态。
        """


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=80,
        chunk_overlap=20,
    )

    chunks = splitter.split_text(text)

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}:")
        print(chunk)
        print("------")
    # result = await chain.ainvoke(
    #     {
    #         "topic": "Agent"
    #     }
    # )

    # result = chain.invoke(
    # {
    #     "topic": "Agent"
    # }
    # )

    # result = await chain.abatch(
    # [
    #     {"topic": "Agent"},
    #     {"topic": "RAG"},
    #     {"topic": "MCP"},
    # ]
    # )

    # result = await parallel.ainvoke(
    #     {"topic": "Agent"}
    # )

    # print(result)

    # async for chunk in chain.astream(
    #     {"topic": "Agent"}
    # ):
    #     print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
