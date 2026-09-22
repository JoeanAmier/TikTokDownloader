from asyncio import to_thread
from math import isfinite
from pathlib import Path
from threading import Lock
from typing import TYPE_CHECKING

from .translation import _

if TYPE_CHECKING:
    from .record import BaseLogger


def format_timestamp(milliseconds: int) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


class Transcriber:
    """可选的本地语音转写；模型按需加载，同一实例串行处理视频。"""

    def __init__(
        self,
        logger: "BaseLogger",
        enabled: bool = False,
        model: str = "small",
        language: str = "",
    ):
        self.log = logger
        self.enabled = enabled
        self.model_name = model
        self.language = language or None
        self._model = None
        self._unavailable = False
        # to_thread 被取消时不会终止推理线程，线程锁仍可避免同时运行模型。
        self._lock = Lock()

    async def run(self, paths: list[Path]) -> None:
        if not self.enabled:
            return
        for path in dict.fromkeys(paths):
            try:
                await to_thread(self._transcribe, path)
            except Exception as e:
                # 后处理失败不能触发重新下载或回滚成功的下载记录。
                self.log.warning(
                    _("{name} 语音转写失败，已下载视频不受影响：{error}").format(
                        name=path.name, error=str(e)
                    )
                )

    def _load_model(self) -> bool:
        if self._unavailable:
            return False
        if self._model is not None:
            return True
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            self._unavailable = True
            self.log.warning(
                _(
                    "语音转写不可用，请在运行程序的 Python 环境安装 "
                    "requirements-transcription.txt 中的可选依赖。"
                )
            )
            return False
        try:
            self.log.info(
                _("正在加载语音转写模型：{model}").format(model=self.model_name)
            )
            self._model = WhisperModel(
                self.model_name, device="cpu", compute_type="int8"
            )
        except Exception:
            # 模型下载/加载失败只尝试一次，避免每个视频重复下载模型。
            self._unavailable = True
            raise
        return True

    def _transcribe(self, path: Path) -> None:
        with self._lock:
            txt, srt = path.with_suffix(".txt"), path.with_suffix(".srt")
            if txt.exists() and srt.exists():
                return
            if not self._load_model():
                return
            self.log.info(_("正在转写视频：{name}").format(name=path.name))
            segments, _info = self._model.transcribe(
                str(path), language=self.language, beam_size=5, vad_filter=True
            )
            lines, subtitles = [], []
            # faster-whisper 在迭代时执行推理；完整成功后才创建输出文件。
            for segment in segments:
                text = " ".join(segment.text.split())
                if not text:
                    continue
                if not all(isfinite(t) for t in (segment.start, segment.end)):
                    raise ValueError("Invalid transcription timestamp")
                start = max(0, round(segment.start * 1000))
                end = max(start + 1, round(segment.end * 1000))
                lines.append(text)
                subtitles.append(
                    f"{len(lines)}\n{format_timestamp(start)} --> "
                    f"{format_timestamp(end)}\n{text}\n\n"
                )
            if not lines:
                self.log.info(
                    _("{name} 未识别到语音，不生成字幕").format(name=path.name)
                )
                return
            self._write_outputs({txt: "\n".join(lines) + "\n", srt: "".join(subtitles)})
            self.log.info(
                _("{name} 语音转写完成，已保存 TXT / SRT").format(name=path.name)
            )

    @staticmethod
    def _write_outputs(outputs: dict[Path, str]) -> None:
        created = []
        try:
            for path, content in outputs.items():
                try:
                    file = path.open("x", encoding="utf-8", newline="\n")
                except FileExistsError:
                    # 保留用户已有的字幕或文稿，包括仅存在其中一个的情况。
                    continue
                created.append(path)
                with file:
                    file.write(content)
        except Exception:
            for path in created:
                path.unlink(missing_ok=True)
            raise
