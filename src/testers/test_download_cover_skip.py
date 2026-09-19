import asyncio
from pathlib import Path

from src.downloader.download import Downloader


class _StubDownloader:
    """Duck-typed stand-in exposing only what download_cover reads, so the
    skip-decision logic can be exercised without constructing a full
    Downloader (which needs live HTTP clients, ffmpeg, a logger, and a
    recorder).
    """

    static_cover = True
    dynamic_cover = True

    def __init__(self, downloaded: bool, file_exists: bool):
        self._downloaded = downloaded
        self._file_exists = file_exists

    async def is_downloaded(self, id_: str) -> bool:
        return self._downloaded

    def is_exists(self, path: Path) -> bool:
        return self._file_exists

    async def is_skip(self, id_: str, path: Path) -> bool:
        return await self.is_downloaded(id_) or self.is_exists(path)


def _run_download_cover(stub: _StubDownloader, item: dict) -> list:
    tasks: list = []

    async def _call():
        await Downloader.download_cover(
            stub,
            tasks,
            "name",
            "id123",
            item,
            Path("/tmp/temp/name"),
            Path("/tmp/actual/name"),
        )

    asyncio.run(_call())
    return tasks


def test_download_cover_skips_when_recorded_downloaded_even_if_path_check_would_miss():
    """Regression for #789: download_video/download_image skip on
    is_skip(), which falls back to the persistent download record when the
    on-disk path check alone would miss (the video's own path check can
    fail the same way, but the record still catches it). download_cover
    only checked is_exists() directly, so a cover kept getting queued for
    re-download every run even when the item was already recorded as
    downloaded.
    """
    item = {"static_cover": "https://example.com/cover.jpg", "dynamic_cover": ""}
    stub = _StubDownloader(downloaded=True, file_exists=False)
    assert _run_download_cover(stub, item) == []


def test_download_cover_still_queues_when_neither_recorded_nor_on_disk():
    item = {"static_cover": "https://example.com/cover.jpg", "dynamic_cover": ""}
    stub = _StubDownloader(downloaded=False, file_exists=False)
    tasks = _run_download_cover(stub, item)
    assert len(tasks) == 1
    assert tasks[0][0] == "https://example.com/cover.jpg"
