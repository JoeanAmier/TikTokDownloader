from src.application import TikTokDownloader
from asyncio import run


async def main():
    async with TikTokDownloader() as downloader:
        await downloader.run()


if __name__ == "__main__":
    run(main())
