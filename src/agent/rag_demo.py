import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_deepseek import ChatDeepSeek


load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY is not set")

def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

format_docs_runnable = RunnableLambda(format_docs)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    },
)

documents = [
    "Agent 可以通过 Tool Calling 调用外部工具。",
    "RAG 会先检索相关知识，再让大模型生成答案。",
    "Redis 是一种高性能内存数据库。",
]

doc_vectors = embeddings.embed_documents(documents)

query_vector = embeddings.embed_query(
    "智能体怎样使用外部工具？"
)

vector_store = InMemoryVectorStore(
    embedding=embeddings
)

vector_store.add_texts(documents)

# results = vector_store.similarity_search_with_score(
#     query="智能体如何调用外部能力？",
#     k=2,
# )

# for doc, score in results:
#     print(f"score={score:.4f}")
#     print(doc.page_content)
#     print("------")

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 2
    }
)

docs = retriever.invoke(
    "智能体怎样调用外部工具？"
)

# for doc in docs:
#     print(doc.page_content)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个严谨的助手。请优先根据提供的上下文回答问题。"
        ),
        (
            "human",
            """
上下文：
{context}

问题：
{question}
"""
        ),
    ]
)

model = ChatDeepSeek(
    model="deepseek-chat",
    api_key=api_key,
    temperature=0,
)

parser = StrOutputParser()

rag_chain = {
    "question": RunnablePassthrough(),
    "context": retriever | format_docs_runnable,
} | prompt | model | parser

async def main():
    result = await rag_chain.ainvoke(
        "Agent 怎么调用外部工具？"
    )

    print(result)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())