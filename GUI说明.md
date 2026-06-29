# 抖音下载器 · 极简桌面外壳 (downkyi 风格)

在 [JoeanAmier/TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader)(DouK-Downloader,GPL-3.0)引擎之上,加了一层**最小化的桌面界面**:

- **粘博主主页链接 → 下载该博主全部作品**
- **粘单个视频链接 → 下载该视频**
- **⭐ 下载我的收藏** —— 纯 Cookie,无需任何链接,把"我的收藏"**按抖音内容分类 + 博主两级**自动分文件夹下载(`分类/UID_博主/`)
- **关注的博主面板**(窗口上部) —— 「⬇ 拉取关注列表」纯 Cookie 直接拉你的抖音**关注列表**(profile/self 取自己 sec_uid → following/list 分页),按分类列出,勾选 → 「🔄 更新选中」一键增量拉新作品;登记表 `Volume/authors.json` 自动维护
- **⏹ 停止** —— 随时中断当前下载(已下完的保留,半成品可续传)

下载、签名(a_bogus)、Cookie、翻页、复权命名等全部复用上游引擎,本外壳只是个壳,不改下载逻辑。

## 怎么用

1. 双击 **`boot.bat`**
   - 第一次会自动在本机 `%LOCALAPPDATA%` 建虚拟环境并装依赖(几分钟,需联网,一次性)
   - 之后秒开窗口
2. 窗口里:**粘链接 → 点对应按钮**;下载我的收藏则**不用链接**,直接点 ⭐
3. 运行日志带 `[第N/共M]` 序号,视频之间空行分隔
4. 底部「打开下载文件夹」可直接定位文件

> 需要 Python 3.12(`boot.bat` 用 `py -3.12` / `python` 自动找)。

## 文件夹规则

统一两级目录 `Volume/{抖音分类}/UID{数字}_{博主名称}/`,分类取作品的 `video_tag` 大类(财经/科技/旅游/科普…),没有标签的进 `未分类/`。

- **博主整号下载**(粘主页): 整个博主归到**主类**(该博主作品里出现最多的分类),一个博主一个文件夹,不拆散。
- **我的收藏**: **按每条作品各自的分类**分(同一博主的收藏可能分散在多个分类下)。
- 同一博主既被整号下载又有收藏时,因 UID 相同**合并进同一个 `分类/UID_博主` 夹**。

## Cookie

- 抖音接口有风控,**必须配登录 Cookie** 才能正常拉数据(否则只下到第一页)。
- 首次在窗口点 **「设置 Cookie」**,把网页登录后的整段 Cookie 粘进去(F12 → Network → 任意 `www.douyin.com` 请求 → Request Headers 里 `cookie:` 后那一长串,含 `sessionid`)。
- Cookie 存在 `Volume/settings.json`,而 `Volume/` 已被 `.gitignore` 排除,**不会进仓库**。
- Cookie 会过期:哪天又"下载失败 / 只下到一页",点「设置 Cookie」重贴一串即可。

## 增量

- 下过的作品记在 `Volume/DouK-Downloader.db` 的 `download_data` 表,**按作品 ID 全局去重**;再次下载自动跳过,只下新增。

## 本分支新增/改动的文件

| 文件 | 说明 |
|------|------|
| `douyin_downloader.pyw` | Tkinter 桌面界面:博主批量 / 单视频 / **我的收藏(按博主分)** / **停止按钮**;引擎引导 + 异步桥;日志 `[第N/共M]` 序号;链接快速解析;设置Cookie |
| `boot.bat` | 自举 venv/依赖,双击启动(纯 ASCII+CRLF,UNC 共享盘安全) |
| `src/custom/static.py` | `MAX_WORKERS` 4 → 8,提升并发 |
| `src/downloader/download.py` | `storage_folder`:post/favorite/collection 统一为 `UID{数字}_{名称}`,去掉 `_发布作品`/`_收藏作品` 后缀 |
| `.gitattributes` | `*.bat` 锁 CRLF |
| `GUI说明.md` | 本文件 |

## 致谢 / 许可

引擎来自 [JoeanAmier/TikTokDownloader](https://github.com/JoeanAmier/TikTokDownloader),遵循 **GPL-3.0**。本外壳同样遵循 GPL-3.0。仅供个人学习研究,请遵守抖音平台规则与版权。
