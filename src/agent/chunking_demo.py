from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    MarkdownHeaderTextSplitter,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

MD_FILE = DATA_DIR / "agent_notes.md"


def show_chunks(title, chunks, max_chunks=4):
    print(f"\n========== {title} ==========")
    print(f"Chunk 数量: {len(chunks)}")

    for i, chunk in enumerate(chunks[:max_chunks]):
        print(f"\n--- Chunk {i + 1} ---")
        print(f"长度: {len(chunk.page_content)}")

        print("内容:")
        print(chunk.page_content)

        print("\nmetadata:")
        print(chunk.metadata)


def recursive_split_demo():
    print("\n\n######## RecursiveCharacterTextSplitter ########")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        add_start_index=True,
    )

    # Markdown
    md_loader = TextLoader(
        str(MD_FILE),
        encoding="utf-8",
    )

    md_documents = md_loader.load()

    md_chunks = splitter.split_documents(md_documents)

    show_chunks(
        "Markdown - Recursive Split",
        md_chunks,
    )

    # PDF
    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("没有找到 PDF")
        return

    pdf_loader = PyPDFLoader(str(pdf_files[0]))
    pdf_documents = pdf_loader.load()

    pdf_chunks = splitter.split_documents(pdf_documents)

    show_chunks(
        "PDF - Recursive Split",
        pdf_chunks,
    )


def markdown_header_split_demo():
    print("\n\n######## MarkdownHeaderTextSplitter ########")

    markdown_text = MD_FILE.read_text(
        encoding="utf-8"
    )

    headers_to_split_on = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3"),
    ]

    splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False,
    )

    chunks = splitter.split_text(markdown_text)

    # MarkdownHeaderTextSplitter 是直接对字符串切分，
    # 所以 source 路径需要我们自己补回 metadata。
    for chunk in chunks:
        chunk.metadata["source"] = str(MD_FILE)

    show_chunks(
        "Markdown - Header Split",
        chunks,
    )

def markdown_two_stage_split_demo():
    print("\n\n######## Markdown Two-Stage Split ########")

    markdown_text = MD_FILE.read_text(
        encoding="utf-8"
    )

    # 第一阶段：按照 Markdown 标题结构切分
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

    # MarkdownHeaderTextSplitter 是直接读取字符串，
    # 因此 source 需要手动补回 metadata
    for chunk in header_chunks:
        chunk.metadata["source"] = str(MD_FILE)

    print(f"第一阶段章节数量: {len(header_chunks)}")

    # 第二阶段：控制每个章节的最大长度
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        add_start_index=True,
    )

    final_chunks = recursive_splitter.split_documents(
        header_chunks
    )

    show_chunks(
        "Markdown - Two Stage Split",
        final_chunks,
        max_chunks=10,
    )

def main():
    recursive_split_demo()
    markdown_header_split_demo()
    markdown_two_stage_split_demo()


if __name__ == "__main__":
    main()