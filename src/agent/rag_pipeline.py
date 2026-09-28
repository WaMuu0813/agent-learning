import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_DIR = PROJECT_ROOT / "storage" / "chroma_db"
COLLECTION_NAME = "agent_knowledge"

load_dotenv(PROJECT_ROOT / ".env")


class RAGService:
    def __init__(self):
        print("正在初始化 RAG Service...")

        if not CHROMA_DIR.exists():
            raise RuntimeError(
                f"Chroma 数据库不存在: {CHROMA_DIR}"
            )

        # 1. 加载本地 Embedding 模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            model_kwargs={
                "device": "cpu",
            },
            encode_kwargs={
                "normalize_embeddings": True,
            },
        )

        # 2. 加载持久化 Chroma
        self.vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(CHROMA_DIR),
        )

        # 检查知识库是不是空的
        data = self.vector_store.get(limit=1)

        if not data.get("ids"):
            raise RuntimeError(
                "Chroma Collection 为空，请先构建知识库"
            )

        # 3. 创建 Retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 3,
            },
        )

        # 4. 创建 DeepSeek 模型
        api_key = os.getenv("DEEPSEEK_API_KEY")

        if not api_key:
            raise RuntimeError(
                "没有找到 DEEPSEEK_API_KEY"
            )

        self.model = ChatDeepSeek(
            model="deepseek-chat",
            api_key=api_key,
            temperature=0,
        )

        # 5. Prompt
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
你是一个本地知识库问答助手。

请优先根据提供的知识库上下文回答问题。

如果上下文中没有足够信息，请明确说明：
“当前知识库中没有足够信息回答这个问题。”

不要编造知识库中不存在的内容。
""",
                ),
                (
                    "human",
                    """
知识库上下文：

{context}

用户问题：

{question}
""",
                ),
            ]
        )

        # 6. LLM Chain
        self.chain = (
            self.prompt
            | self.model
            | StrOutputParser()
        )

        print("RAG Service 初始化完成")


    @staticmethod
    def format_docs(documents):
        return "\n\n".join(
            doc.page_content
            for doc in documents
        )


    async def ask(self, question: str):
        documents = await self.retriever.ainvoke(
            question
        )

        context = self.format_docs(
            documents
        )

        answer = await self.chain.ainvoke(
            {
                "question": question,
                "context": context,
            }
        )

        return answer, documents