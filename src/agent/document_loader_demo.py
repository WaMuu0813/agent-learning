from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader


# Path：Python 标准库里的“路径对象”
# 作用：比手写字符串路径更方便、更不容易写错
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

MD_FILE = DATA_DIR / "agent_notes.md"


def print_documents(title, documents, max_docs=2, preview_chars=500):
    print(f"\n========== {title} ==========")
    print(f"Document 数量: {len(documents)}")

    for i, doc in enumerate(documents[:max_docs]):
        print(f"\n--- Document {i + 1} ---")

        print("page_content:")
        print(doc.page_content[:preview_chars])

        print("\nmetadata:")
        print(doc.metadata)


def load_markdown():
    if not MD_FILE.exists():
        print(f"找不到 Markdown 文件: {MD_FILE}")
        return

    loader = TextLoader(
        str(MD_FILE),
        encoding="utf-8",
    )

    documents = loader.load()

    print_documents(
        title="Markdown",
        documents=documents,
    )


def load_pdfs():
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print(f"\n{DATA_DIR} 中没有找到 PDF")
        return

    for pdf_file in pdf_files:
        loader = PyPDFLoader(str(pdf_file))

        documents = loader.load()

        print_documents(
            title=f"PDF: {pdf_file.name}",
            documents=documents,
        )


def main():
    load_markdown()
    load_pdfs()


if __name__ == "__main__":
    main()