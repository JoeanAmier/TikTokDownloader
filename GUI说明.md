# 抖音下载器 · 极简桌面外壳 (downkyi 风格)

在 [JoeanAmier/TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader)(DouK-Downloader,GPL-3.0)引擎之上,加了一层**最小化的桌面界面**:只保留两件事——

- **粘博主主页链接 → 下载该博主全部作品**
- **粘单个视频链接 → 下载该视频**

下载、签名(a_bogus)、Cookie、翻页、复权命名等全部复用上游引擎,本外壳只是个壳,不改下载逻辑。

## 怎么用

1. 双击 **`boot.bat`**
   - 第一次会自动在本机 `%LOCALAPPDATA%` 建虚拟环境并装依赖(几分钟,需联网,一次性)
   - 之后秒开窗口
2. 窗口里:**粘链接 → 点对应按钮**(「下载该博主全部作品」/「下载单个视频」)
3. 运行日志带 `[第N/共M]` 序号,视频之间空行分隔
4. 底部「打开下载文件夹」可直接定位文件(默认落在 `Volume/Download/` 下的账号文件夹)

> 需要 Python 3.12(`boot.bat` 用 `py -3.12` / `python` 自动找)。

## Cookie

- 抖音接口有风控,**必须配登录 Cookie** 才能正常拉数据(否则只下到第一页)。
- 首次在窗口点 **「设置 Cookie」**,把网页登录后的整段 Cookie 粘进去即可(F12 → Network → 任意 `www.douyin.com` 请求 → Request Headers 里 `cookie:` 后那一长串,含 `sessionid`)。
- Cookie 存在 `Volume/settings.json`,而 `Volume/` 已被 `.gitignore` 排除,**不会进仓库**。
- Cookie 会过期:哪天又"下载失败 / 只下到一页",点「设置 Cookie」重贴一串即可。

## 本分支新增/改动的文件

| 文件 | 说明 |
|------|------|
| `douyin_downloader.pyw` | Tkinter 桌面界面 + 引擎引导 + 异步桥 + 日志序号 |
| `boot.bat` | 自举 venv/依赖,双击启动(UNC 共享盘安全,纯 ASCII+CRLF) |
| `src/custom/static.py` | `MAX_WORKERS` 4 → 8,提升并发下载 |

## 致谢 / 许可

引擎来自 [JoeanAmier/TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader),遵循 **GPL-3.0**。本外壳同样遵循 GPL-3.0。仅供个人学习研究,请遵守抖音平台规则与版权。
