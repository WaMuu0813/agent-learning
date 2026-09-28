import asyncio

from rag_pipeline import ask


async def main():
    question = input(
        "请输入问题: "
    )

    answer, documents = await ask(
        question
    )

    print("\n========== Answer ==========")
    print(answer)

    print("\n========== Sources ==========")

    for i, doc in enumerate(
        documents,
        start=1,
    ):
        print(f"\nSource {i}")

        print(
            "source:",
            doc.metadata.get(
                "source",
                "unknown",
            ),
        )

        print(
            "page:",
            doc.metadata.get(
                "page",
                "N/A",
            ),
        )

        print(
            "section:",
            doc.metadata.get(
                "h2",
                doc.metadata.get(
                    "h1",
                    "N/A",
                ),
            ),
        )

        print(
            "content:",
            doc.page_content[:200],
        )


if __name__ == "__main__":
    asyncio.run(main())