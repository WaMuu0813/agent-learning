import asyncio
import time


async def task(name: str):
    print(f"{name} start")

    if(name == "A") :
        await asyncio.sleep(3)
    else :
        await asyncio.sleep(5)

    print(f"{name} end")


async def main():
    start = time.time()

    await asyncio.gather(
        task("A"),
        task("B"),
    )

    print(f"total: {time.time() - start:.2f}s")


asyncio.run(main())