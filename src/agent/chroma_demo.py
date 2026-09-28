from pathlib import Path

from langchain_chroma import Chroma

from faiss_demo import build_chunks, build_embeddings


PROJECT_ROOT = Path(__file__).resolve().parents[2]

CHROMA_DIR = PROJECT_ROOT / "storage" / "chroma_db"

COLLECTION_NAME = "agent_knowledge"


def build_database():
    chunks = build_chunks()
    embeddings = build_embeddings()

    print(f"准备写入 Chroma 的 Chunk 数量: {len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR),
    )

    print(f"Chroma 数据库已保存到: {CHROMA_DIR}")

    return vector_store


def load_database():
    embeddings = build_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=str(CHROMA_DIR),
    )

    print("已有 Chroma 数据库加载成功")

    return vector_store


def search(vector_store, query):
    results = vector_store.similarity_search_with_score(
        query=query,
        k=3,
    )

    print(f"\nQuery: {query}")

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n========== Result {i} ==========")
        print(f"score: {score:.4f}")

        print("\ncontent:")
        print(doc.page_content[:500])

        print("\nmetadata:")
        print(doc.metadata)


def main():
    if CHROMA_DIR.exists():
        vector_store = load_database()
    else:
        vector_store = build_database()

    search(
        vector_store,
        "Agent 如何调用外部工具？",
    )


if __name__ == "__main__":
    main()