# 下载后语音转写 / Post-download transcription

## 中文

此功能使用 [faster-whisper](https://github.com/SYSTRAN/faster-whisper) 在本地识别视频中的语音，将结果保存为视频旁的同名 UTF-8 TXT 文稿和 SRT 字幕。例如 `视频.mp4` 对应 `视频.txt` 和 `视频.srt`。

### 安装

目前面向 **Python 源码运行方式**；现有可执行文件和 Docker 镜像不包含转写依赖。普通下载用户无需安装额外组件。

使用 pip：在运行 DouK-Downloader 的同一个 Python 环境中安装可选依赖，随后按原方式启动：

```shell
python -m pip install -r requirements-transcription.txt
python main.py
```

使用 uv：

```shell
uv run --with-requirements requirements-transcription.txt main.py
```

语音解码使用 PyAV 自带的 FFmpeg 库，此功能无需另外配置 FFmpeg 可执行文件。

### 配置

先运行一次程序生成 `Volume/settings.json`，修改以下三个字段，然后重新启动：

```json
{
  "transcribe": true,
  "transcription_model": "small",
  "transcription_language": "zh"
}
```

以上仅为需要修改的字段，**不要替换整个配置文件**。

| 字段 | 默认值 | 说明 |
| --- | --- | --- |
| `transcribe` | `false` | 是否对本次成功下载的视频执行语音转写 |
| `transcription_model` | `"small"` | faster-whisper 支持的模型名称（如 `tiny`、`small`、`large-v3`），或本地 CTranslate2 模型目录 |
| `transcription_language` | `""` | 留空自动识别，或指定语言代码（如 `zh`、`en`） |

初次使用模型名称会从 Hugging Face 下载并缓存模型，需要联网和额外磁盘空间；如果无法连接，可提前准备兼容的模型目录并配置本地路径。语音识别在本机执行，不调用云端转写服务，也不需要 API Key。

### 行为与限制

- 仅处理本次成功下载的抖音 / TikTok 视频作品；已存在或有下载记录而被跳过的视频不会自动补转写。图集、封面、音乐文件、实况图片和直播流不在此功能范围内。
- 当前下载批次完成后串行转写，采用 CPU / INT8，模型在同一个下载器实例内复用。转写会增加总运行时间和内存占用；大模型尤其明显。
- 原视频与下载记录保持不变。缺少依赖、模型加载失败、无音轨或写文件失败时会记录提示，不会因转写失败重新下载视频。
- 模型加载失败后，当前下载器实例不再重复尝试加载；修复依赖或模型后重新启动程序。
- 已有 TXT / SRT 不会被覆盖。若只缺少一个文件，仅生成缺失文件；两个文件都存在时跳过推理。
- 未识别到语音时不生成空文稿或空字幕。转写可能出现错字，字幕时间来自模型，需人工校对。
- 不包含画面 OCR、翻译、LLM 摘要或文稿润色。

## English

This optional feature uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) to transcribe newly downloaded Douyin / TikTok videos locally. It writes UTF-8 `video.txt` and `video.srt` next to `video.mp4`.

### Installation and configuration

This feature currently targets **Python source installations**. Existing executables and Docker images do not include its dependencies. Install the optional requirements in the same Python environment used to run the downloader:

```shell
python -m pip install -r requirements-transcription.txt
python main.py
```

For uv installations, start with:

```shell
uv run --with-requirements requirements-transcription.txt main.py
```

PyAV provides the audio decoder; no separate FFmpeg executable is needed for transcription.

Run the application once to create `Volume/settings.json`. Set `transcribe` to `true`, optionally set `transcription_model` (default: `"small"`) and `transcription_language` (default: `""`, auto-detect), then restart. Use a language code such as `"en"` or `"zh"`. Keep all other settings.

A model name downloads and caches the model from Hugging Face on first use, requiring network access and disk space. A local CTranslate2 model directory can be supplied instead. Inference runs locally on CPU with INT8; no cloud transcription service or API key is used.

### Behavior and limitations

- Only videos successfully downloaded in the current batch are processed, sequentially after network downloads finish. Files skipped by existing download records or file checks are not backfilled. Images, covers, music, live photos and live streams are excluded.
- One model is loaded lazily and reused per downloader instance. Transcription adds processing time and memory usage, especially with larger models.
- Missing dependencies, model loading, inference or output errors do not undo successful downloads or trigger network download retries. Fix the environment and restart after a model-loading failure; the same downloader instance will not repeatedly attempt loading it.
- Existing TXT / SRT files are preserved. Only missing sidecars are created; if both exist, inference is skipped. No empty files are created when no speech is recognized.
- Transcripts and timings may need manual correction. OCR, translation, LLM summaries and text rewriting are outside this feature's scope.

## Tests

The unit and download-integration tests use a fake speech backend and require no model downloads or optional transcription dependencies:

```shell
python -m pytest src/testers -q
```
