from asyncio import Event, Semaphore, run, wait_for
from types import SimpleNamespace

from httpx import AsyncClient, MockTransport, Response
from pytest import mark

from src.downloader import Downloader
from src.tools import FakeProgress


class Recorder:
    async def update_id(self, id_):
        pass

    async def delete_id(self, id_):
        pass


def create_downloader(static_cover: bool, dynamic_cover: bool) -> Downloader:
    downloader = Downloader.__new__(Downloader)
    downloader.static_cover = static_cover
    downloader.dynamic_cover = dynamic_cover
    downloader.headers = {}
    downloader.headers_tiktok = {}
    downloader.log = SimpleNamespace(
        info=lambda *args: None,
        warning=lambda *args: None,
        error=lambda *args: None,
    )
    downloader.console = SimpleNamespace(warning=lambda *args: None)
    downloader.chunk = 1024
    downloader.max_retry = 0
    downloader.max_size = 0
    downloader.recorder = Recorder()
    downloader.truncate = 80
    return downloader


@mark.parametrize(
    ("static_cover", "dynamic_cover", "expected"),
    [
        (True, False, "work.jpeg"),
        (False, True, "work.webp"),
    ],
)
def test_download_cover_preserves_single_cover_names(
    tmp_path, static_cover, dynamic_cover, expected
):
    downloader = create_downloader(static_cover, dynamic_cover)
    tasks = []

    downloader.download_cover(
        tasks,
        "work",
        "1",
        {
            "static_cover": "https://example.com/static",
            "dynamic_cover": "https://example.com/dynamic",
        },
        tmp_path.joinpath("cache", "work"),
        tmp_path.joinpath("output", "work"),
    )

    assert len(tasks) == 1
    assert tasks[0][2].name == expected


def test_download_cover_treats_ambiguous_webp_as_legacy_dynamic(tmp_path):
    downloader = create_downloader(True, True)
    output = tmp_path.joinpath("output")
    output.mkdir()
    output.joinpath("work.webp").write_bytes(
        b"RIFF\x0c\x00\x00\x00WEBPVP8 \x00\x00\x00\x00"
    )
    tasks = []

    downloader.download_cover(
        tasks,
        "work",
        "1",
        {
            "static_cover": "https://example.com/static",
            "dynamic_cover": "https://example.com/dynamic",
        },
        tmp_path.joinpath("cache", "work"),
        output.joinpath("work"),
    )

    assert len(tasks) == 1
    assert tasks[0][2].name == "work.jpeg"


def test_concurrent_jpeg_covers_use_distinct_files(tmp_path):
    async def download_covers():
        started = 0
        both_started = Event()

        async def handler(request):
            nonlocal started
            started += 1
            if started == 2:
                both_started.set()
            await wait_for(both_started.wait(), 1)
            content = b"static" if request.url.path == "/static" else b"dynamic"
            return Response(
                200,
                headers={
                    "Content-Type": "image/jpeg",
                    "Content-Length": str(len(content)),
                },
                content=content,
            )

        cache = tmp_path.joinpath("cache")
        output = tmp_path.joinpath("output")
        cache.mkdir()
        output.mkdir()
        downloader = create_downloader(True, True)
        item = {
            "static_cover": "https://example.com/static",
            "dynamic_cover": "https://example.com/dynamic",
        }
        tasks = []
        async with AsyncClient(transport=MockTransport(handler)) as client:
            downloader.client = client
            downloader.client_tiktok = client
            downloader.download_cover(
                tasks,
                "work",
                "1",
                item,
                cache.joinpath("work"),
                output.joinpath("work"),
            )
            await downloader.downloader_chart(
                tasks,
                SimpleNamespace(),
                FakeProgress(),
                semaphore=Semaphore(2),
            )
            second_run_tasks = []
            downloader.download_cover(
                second_run_tasks,
                "work",
                "1",
                item,
                cache.joinpath("work"),
                output.joinpath("work"),
            )
            await downloader.downloader_chart(
                second_run_tasks,
                SimpleNamespace(),
                FakeProgress(),
                semaphore=Semaphore(2),
            )

        assert started == 2
        assert second_run_tasks == []
        assert output.joinpath("work.jpeg").read_bytes() == b"static"
        assert output.joinpath("work_dynamic.jpeg").read_bytes() == b"dynamic"

    run(download_covers())
