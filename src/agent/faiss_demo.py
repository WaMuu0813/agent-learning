from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
MD_FILE = DATA_DIR / "agent_notes.md"

FAISS_DIR = PROJECT_ROOT / "storage" / "faiss_index"


def build_chunks():
    all_chunks = []

    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        add_start_index=True,
    )

    # ---------- Markdown ----------
    if MD_FILE.exists():
        markdown_text = MD_FILE.read_text(
            encoding="utf-8"
        )

        header_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
            ],
            strip_headers=False,
        )

        header_chunks = header_splitter.split_text(
            markdown_text
        )

        for chunk in header_chunks:
            chunk.metadata["source"] = str(MD_FILE)

        md_chunks = recursive_splitter.split_documents(
            header_chunks
        )

        all_chunks.extend(md_chunks)

    # ---------- PDF ----------
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    for pdf_file in pdf_files:
        loader = PyPDFLoader(str(pdf_file))
        documents = loader.load()

        pdf_chunks = recursive_splitter.split_documents(
            documents
        )

        all_chunks.extend(pdf_chunks)

    return all_chunks


def build_embeddings():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )


def build_index(chunks, embeddings):
    print(f"准备写入 FAISS 的 Chunk 数量: {len(chunks)}")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vector_store


def search(vector_store, query):
    results = vector_store.similarity_search_with_score(
        query,
        k=3,
    )

    print(f"\nQuery: {query}")

    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n========== Result {i} ==========")
        print(f"score: {score:.4f}")
        print("content:")
        print(doc.page_content[:500])

        print("\nmetadata:")
        print(doc.metadata)


# def main():
#     chunks = build_chunks()

#     if not chunks:
#         print("没有找到可建立索引的文档")
#         return

#     embeddings = build_embeddings()

#     vector_store = build_index(
#         chunks,
#         embeddings,
#     )

#     # 保存到硬盘
#     FAISS_DIR.mkdir(
#         parents=True,
#         exist_ok=True,
#     )

#     vector_store.save_local(
#         str(FAISS_DIR)
#     )

#     print(f"\nFAISS 索引已保存到: {FAISS_DIR}")

#     search(
#         vector_store,
#         "Agent 如何调用外部工具？"
#     )

def main():
    embeddings = build_embeddings()

    vector_store = FAISS.load_local(
        str(FAISS_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print("FAISS 索引加载成功")

    search(
        vector_store,
        "Agent 如何调用外部工具？"
    )


if __name__ == "__main__":
    main()