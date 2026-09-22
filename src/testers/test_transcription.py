import asyncio
import json
import sys
from pathlib import Path
from threading import Event
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from curl_cffi.requests.exceptions import RequestException

from src.downloader import Downloader
from src.config import Settings
from src.models.settings import Settings as SettingsModel
from src.transcription import Transcriber, format_timestamp
from src.translation import _


def segment(start=0.0, end=1.5, text=" 你好，世界。 "):
    return SimpleNamespace(start=start, end=end, text=text)


@pytest.fixture
def backend(monkeypatch):
    model = Mock()
    model.transcribe.side_effect = lambda *a, **kw: (iter([segment()]), None)
    constructor = Mock(return_value=model)
    monkeypatch.setitem(
        sys.modules, "faster_whisper", SimpleNamespace(WhisperModel=constructor)
    )
    return constructor, model


def test_disabled_does_not_import_optional_dependency(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "faster_whisper", None)
    log = Mock()
    transcriber = Transcriber(log)
    asyncio.run(transcriber.run([tmp_path / "video.mp4"]))
    log.warning.assert_not_called()
    assert transcriber._model is None
    assert not list(tmp_path.iterdir())


def test_old_settings_migrate_with_transcription_disabled(tmp_path):
    root = tmp_path / "Volume"
    root.mkdir()
    settings = Settings(root, Mock())
    settings.path.write_text('{"download": true}', encoding="utf-8")
    migrated = settings.read()
    assert migrated["download"] is True
    assert migrated["transcribe"] is False
    assert migrated["transcription_model"] == "small"
    assert migrated["transcription_language"] == ""
    saved = json.loads(settings.path.read_text(encoding=settings.encode))
    assert saved["transcribe"] is False


def test_transcription_settings_survive_api_model_roundtrip():
    values = {
        "transcribe": True,
        "transcription_model": "models/local-model",
        "transcription_language": "zh",
    }
    output = SettingsModel(**values).model_dump()
    assert all(output[key] == value for key, value in values.items())


def test_missing_dependency_warns_once(tmp_path, monkeypatch):
    monkeypatch.setitem(sys.modules, "faster_whisper", None)
    log = Mock()
    asyncio.run(
        Transcriber(log, enabled=True).run([tmp_path / "a.mp4", tmp_path / "b.mp4"])
    )
    assert log.warning.call_count == 1
    assert "requirements-transcription.txt" in log.warning.call_args.args[0]


def test_exports_utf8_srt_and_reuses_model(tmp_path, backend):
    constructor, model = backend
    video = tmp_path / "中文 视频.mp4"
    video.write_bytes(b"original video")
    transcriber = Transcriber(Mock(), enabled=True, model="local-model", language="zh")
    asyncio.run(transcriber.run([video, video, tmp_path / "second.mp4"]))
    constructor.assert_called_once_with(
        "local-model", device="cpu", compute_type="int8"
    )
    assert model.transcribe.call_count == 2
    assert model.transcribe.call_args.kwargs["language"] == "zh"
    assert video.with_suffix(".txt").read_text(encoding="utf-8") == "你好，世界。\n"
    assert video.with_suffix(".srt").read_text(encoding="utf-8") == (
        "1\n00:00:00,000 --> 00:00:01,500\n你好，世界。\n\n"
    )
    assert video.read_bytes() == b"original video"
    asyncio.run(transcriber.run([video]))
    assert model.transcribe.call_count == 2


@pytest.mark.parametrize("suffix", [".txt", ".srt"])
def test_preserves_existing_sidecar(tmp_path, backend, suffix):
    path = tmp_path / "video.mp4"
    existing = path.with_suffix(suffix)
    existing.write_text("manually corrected", encoding="utf-8")
    asyncio.run(Transcriber(Mock(), enabled=True).run([path]))
    assert existing.read_text(encoding="utf-8") == "manually corrected"
    assert path.with_suffix(".txt").exists()
    assert path.with_suffix(".srt").exists()


def test_generator_failure_leaves_no_partial_output_and_continues(tmp_path, backend):
    def broken():
        yield segment()
        raise ValueError("audio decoding failed")

    _, model = backend
    model.transcribe.side_effect = [(broken(), None), (iter([segment()]), None)]
    log = Mock()
    asyncio.run(
        Transcriber(log, enabled=True).run(
            [tmp_path / "bad.mp4", tmp_path / "good.mp4"]
        )
    )
    assert not (tmp_path / "bad.txt").exists()
    assert not (tmp_path / "bad.srt").exists()
    assert (tmp_path / "good.srt").exists()
    assert log.warning.call_count == 1


def test_model_load_failure_is_not_repeated_for_each_video(tmp_path, backend):
    constructor, _model = backend
    constructor.side_effect = OSError("model unavailable")
    log = Mock()
    asyncio.run(
        Transcriber(log, enabled=True).run([tmp_path / "a.mp4", tmp_path / "b.mp4"])
    )
    assert constructor.call_count == 1
    assert log.warning.call_count == 1


@pytest.mark.parametrize(
    "segments", [[], [segment(text=" \n ")], [segment(start=float("nan"))]]
)
def test_empty_or_invalid_transcript_creates_no_files(tmp_path, backend, segments):
    _, model = backend
    model.transcribe.side_effect = lambda *a, **kw: (iter(segments), None)
    asyncio.run(Transcriber(Mock(), enabled=True).run([tmp_path / "video.mp4"]))
    assert not list(tmp_path.iterdir())


def test_timestamp_rounding_and_blank_cues(tmp_path, backend):
    _, model = backend
    model.transcribe.side_effect = lambda *a, **kw: (
        iter(
            [
                segment(text=""),
                segment(59.9996, 60.5, "first\n\nline"),
                segment(-1, 0, "second"),
            ]
        ),
        None,
    )
    asyncio.run(Transcriber(Mock(), enabled=True).run([tmp_path / "video.mp4"]))
    text = (tmp_path / "video.srt").read_text(encoding="utf-8")
    assert text.startswith("1\n00:01:00,000 --> 00:01:00,500\nfirst line\n\n")
    assert "2\n00:00:00,000 --> 00:00:00,001\nsecond" in text
    assert format_timestamp(3600001) == "01:00:00,001"


def test_output_write_failure_rolls_back_only_new_files(tmp_path, monkeypatch):
    txt, srt = tmp_path / "video.txt", tmp_path / "video.srt"
    original_open = Path.open

    def fail_srt(path, *args, **kwargs):
        if path == srt:
            raise PermissionError("read-only directory")
        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", fail_srt)
    with pytest.raises(PermissionError):
        Transcriber._write_outputs({txt: "transcript", srt: "subtitles"})
    assert not txt.exists()
    txt.write_text("existing", encoding="utf-8")
    with pytest.raises(PermissionError):
        Transcriber._write_outputs({txt: "transcript", srt: "subtitles"})
    assert txt.read_text(encoding="utf-8") == "existing"


def test_inference_does_not_block_event_loop(tmp_path, backend):
    _, model = backend
    release = Event()
    started = Event()

    def transcribe(*args, **kwargs):
        started.set()
        assert release.wait(2), "event loop was blocked by inference"
        return iter([segment()]), None

    model.transcribe.side_effect = transcribe

    async def run():
        task = asyncio.create_task(
            Transcriber(Mock(), enabled=True).run([tmp_path / "v.mp4"])
        )
        while not started.is_set():
            await asyncio.sleep(0.001)
        release.set()
        await task

    asyncio.run(run())
    assert (tmp_path / "v.srt").exists()


def make_downloader(transcriber, failure=False, content_type="video/quicktime"):
    async def chunks(_size):
        yield b"video"
        if failure:
            raise RequestException("connection interrupted")

    response = Mock(status_code=200)
    response.headers = {"Content-Type": content_type, "Content-Length": "5"}
    response.aiter_content = chunks
    downloader = Downloader.__new__(Downloader)
    downloader.transcriber = transcriber
    downloader.client = downloader.client_tiktok = SimpleNamespace(
        request=AsyncMock(return_value=response)
    )
    downloader.headers = downloader.headers_tiktok = {}
    downloader.log = Mock()
    downloader.console = Mock()
    downloader.recorder = SimpleNamespace(update_id=AsyncMock(), delete_id=AsyncMock())
    downloader.max_retry = 0
    downloader.max_size = 0
    downloader.chunk = 1024
    downloader.truncate = 50
    return downloader


def download_batch(tmp_path, downloader, kind="视频", tiktok=False):
    progress = Mock()
    progress.__enter__ = Mock()
    progress.__exit__ = Mock()
    count = SimpleNamespace(
        downloaded_video=set(), downloaded_image=set(), downloaded_live=set()
    )
    task = (
        "https://example.invalid/video",
        tmp_path / "cache",
        tmp_path / "video.mp4",
        f"【{_(kind)}】video",
        "123",
        "mp4",
    )
    asyncio.run(
        downloader.downloader_chart(
            [task], count, progress, semaphore=asyncio.Semaphore(1), tiktok=tiktok
        )
    )
    return count, progress


@pytest.mark.parametrize("tiktok", [False, True])
def test_download_hook_uses_final_filename_after_success(tmp_path, tiktok):
    transcriber = SimpleNamespace(run=AsyncMock())
    downloader = make_downloader(transcriber)
    count, progress = download_batch(tmp_path, downloader, tiktok=tiktok)
    transcriber.run.assert_awaited_once_with([tmp_path / "video.mov"])
    assert (tmp_path / "video.mov").read_bytes() == b"video"
    assert count.downloaded_video == {"123"}
    downloader.recorder.update_id.assert_awaited_once_with("123")
    progress.__exit__.assert_called_once()


@pytest.mark.parametrize("kind", ["图集", "音乐", "动图", "实况"])
def test_other_download_types_are_not_transcribed(tmp_path, kind):
    transcriber = SimpleNamespace(run=AsyncMock())
    download_batch(tmp_path, make_downloader(transcriber), kind=kind)
    transcriber.run.assert_awaited_once_with([])


def test_interrupted_download_is_not_transcribed(tmp_path):
    transcriber = SimpleNamespace(run=AsyncMock())
    downloader = make_downloader(transcriber, failure=True)
    count, _progress = download_batch(tmp_path, downloader)
    transcriber.run.assert_awaited_once_with([])
    downloader.recorder.update_id.assert_not_awaited()
    assert not count.downloaded_video
    assert not (tmp_path / "video.mov").exists()


def test_transcription_failure_keeps_download_and_record(tmp_path, backend):
    _, model = backend
    model.transcribe.side_effect = ValueError("no audio stream")
    downloader = make_downloader(Transcriber(Mock(), enabled=True))
    count, _progress = download_batch(tmp_path, downloader)
    assert (tmp_path / "video.mov").read_bytes() == b"video"
    assert count.downloaded_video == {"123"}
    downloader.recorder.update_id.assert_awaited_once_with("123")


def test_size_limit_skip_is_not_transcribed(tmp_path):
    transcriber = SimpleNamespace(run=AsyncMock())
    downloader = make_downloader(transcriber)
    downloader.max_size = 1
    download_batch(tmp_path, downloader)
    transcriber.run.assert_awaited_once_with([])
    assert not list(tmp_path.iterdir())
