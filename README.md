<div align="center">
<img src="static/images/TikTokDownloader.png" alt="TikTokDownloader" height="128" width="128"><br>
<h1>TikTokDownloader</h1>
<a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/license">
<img src="https://img.shields.io/github/license/JoeanAmier/TikTokDownloader" alt="GNU General Public License v3.0">
</a>
<a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">
<img src="https://img.shields.io/github/v/release/JoeanAmier/TikTokDownloader" alt="TikTokDownloader">
</a>
<img src="https://img.shields.io/badge/%E8%BD%BB%E9%87%8F%E7%BA%A7-%E9%A1%B9%E7%9B%AE-green" alt="轻量级项目">
</div>
<br>
<p>🔥 <b>抖音视频/图集/直播下载工具：</b>批量下载抖音账号发布页或者喜欢页的作品；单独下载抖音链接对应的作品；获取抖音直播推流地址；下载抖音直播视频。</p>
<p>⭐ <b>使用者在使用本项目的代码时，请遵守 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/license">GNU General Public License v3.0</a> 开源协议。</b></p>
<hr>

# 📝 功能清单

* ✅ 全部代码开源，仅限学习交流
* ✅ 下载抖音无水印视频/图集
* ✅ 批量下载账号发布页/喜欢页作品
* ✅ 单独下载链接对应的作品
* ✅ 多账号批量下载作品
* ✅ 自动跳过已下载的文件
* ✅ 记录详细数据至文件
* ✅ 下载动态/静态封面图
* ✅ 获取直播推流地址
* ✅ 下载抖音直播视频
* ☑️ Web UI 交互界面
* ☑️ 下载 TikTok 无水印视频/图集

# 📈 项目状态

* 🟢 目前全部功能已通过测试，均可正常使用
* 🟢 正在开发 Web UI 交互界面
* 🟡 准备开发多进程模式，提高多账号批量下载效率
* 🔴 暂未发现影响使用的Bug，如果在使用过程中发现Bug，请及时告知作者修复

# 📁 项目结构

```text
TikTokDownloader
├─ CookieTool.py                           // Cookie 写入工具
├─ main.py                                 // 项目程序启动入口
├─ requirements.txt                        // 程序所需第三方模块信息
├─ settings.json                           // 运行参数配置文件
├─ src                                     // 项目模块源码文件夹
│    ├─ Configuration.py                   // 配置文件处理模块
│    ├─ DataAcquirer.py                    // 抖音数据获取模块
│    ├─ DataDownloader.py                  // 抖音作品下载模块
│    ├─ Parameter.py                       // 加密参数生成模块
│    ├─ Recorder.py                        // 日志及数据记录模块
│    ├─ StringCleaner.py                   // 非法字符处理模块
│    ├─ main_complete.py                   // 单线程启动入口
│    ├─ main_multiprocess.py               // 多进程启动入口
│    └─ main_web_UI.py                     // Web UI 启动入口
├─ static                                  // 静态资源文件夹
└─ templates                               // HTML 模板文件夹
```

# 📋 使用说明

**程序运行模式：**

* 单线程终端模式: 支持所有功能
* 多进程终端模式: 仅支持多账号批量下载功能
* Web UI 交互模式: 仅支持单独下载功能和获取直播推流地址功能

<hr>

**Cookie：**

|    程序功能    | 是否需要登录 |
|:----------:|:------:|
| 批量下载发布页作品  |   ❌    |
| 批量下载喜欢页作品  |   ❌    |
| 单独下载链接对应作品 |   ❌    |
|  提取直播推流地址  |   ❌    |
|   下载直播视频   |   ❌    |

<hr>

**注意事项：**

* 首次使用前需要打开抖音网页版(无需登录)，并复制Cookie至配置文件
* 程序请求输入时，不输入内容即为退出程序
* 批量下载时，文件将会下载至账号同名文件夹（自动创建）
* 单独下载时，文件将会下载至指定名称文件夹（默认文件夹名称：Download）
* 如果资源没有描述，保存时文件名称的描述将替换为作品ID
* 注意区分 **账号链接** 和 **视频/图集链接**
* 如果账号修改了昵称，将会重新下载全部作品；手动修改账号昵称文件夹名称，并且保存作品时不要在文件名称中使用昵称，可避免此问题
* 作品下载失败时优先尝试重新填写Cookie至配置文件后重试
* 由于获取账号喜欢页作品数据时仅返回喜欢作品的发布日期，不返回点赞日期，因此程序需要获取全部喜欢作品数据再进行日期筛选，如果账号喜欢页作品较多，可能会花费较长的时间。
* 批量下载账号发布页作品时，如果设置了作品最早发布日期限制，早于该日期的作品无需获取数据
* 如果单独下载功能正常，批量下载功能异常，请尝试使用代理，可能是IP被封禁了
* 如果需要使用批量下载模式在短时间内下载大量作品，建议使用代理

# 🔗 链接类型

**抖音APP**或**抖音网页版**点击分享按钮生成的链接具有时效性，过期需要重新生成使用，**抖音网页版**从浏览器地址栏复制的链接永久有效。

|                       链接格式                       |   链接内容   | 有效期  |   程序支持    |
|:------------------------------------------------:|:--------:|:----:|:---------:|
|           `https://v.douyin.com/分享码/`            | 账号、视频、图集 | 临时有效 | 批量下载、单独下载 |
|        `https://www.douyin.com/note/作品ID`        |    图集    | 永久有效 |   单独下载    |
|       `https://www.douyin.com/video/作品ID`        |    视频    | 永久有效 |   单独下载    |
|        `https://www.douyin.com/user/账号ID`        |    账号    | 永久有效 |   批量下载    |
| `https://www.douyin.com/user/账号ID?modal_id=作品ID` | 账号、视频、图集 | 永久有效 | 批量下载、单独下载 |
|          `https://live.douyin.com/直播ID`          |    直播    | 临时有效 |   直播下载    |

# ⚙️ Settings.json

|                     参数                      |                   类型                   |                                           说明                                            |
|:-------------------------------------------:|:--------------------------------------:|:---------------------------------------------------------------------------------------:|
|                     url                     |                  str                   |                     账号主页链接，批量下载时使用（非视频/图集链接）<br>**属于 accounts 子参数**                     |
|                    mode                     |                  str                   |           批量下载类型，post 代表发布页，favorite 代表喜欢页<br>需要账号喜欢页公开可见，**属于 accounts 子参数**           |
|                  earliest                   |                  str                   |                作品最早发布日期，格式: 2023/1/1，设置为空字符串代表不限制<br>**属于 accounts 子参数**                |
|                   latest                    |                  str                   |                作品最晚发布日期，格式: 2023/1/1，设置为空字符串代表不限制<br>**属于 accounts 子参数**                |
| accounts<br>\[url, mode, earliest, latest\] | list\[list<br>\[str, str, str, str\]\] |                账号链接、批量下载类型、最早发布日期、最晚发布日期<br>账号批量下载时使用，支持多账号，以列表格式包含四个参数                 |
|                    root                     |                  str                   |                                 作品文件和数据记录保存路径，默认值：当前路径                                  |
|                   folder                    |                  str                   |                              单独下载作品时，储存文件夹的名称，默认值：Download                              |
|                    name                     |                  str                   | 文件保存时的命名规则，值之间使用空格分隔<br>默认值：发布时间-作者-描述<br>id: 唯一值；desc: 描述；create_time: 发布时间；author: 作者 |
|                    time                     |                  str                   |                 发布时间的格式，默认值：年-月-日 时.分.秒<br>（注意：Windows下文件名不能包含英文冒号“:”）                  |
|                    split                    |                  str                   |                                    文件命名的分隔符，默认值：“-”                                     |
|                    music                    |              list\[bool\]              |                                 是否下载视频和图集的音乐，默认值：False                                  |
|                    save                     |                  str                   |                   详细数据保存格式，设置为空字符串代表不保存<br>目前支持: csv、xlsx、sql(SQLite)                   |
|                   cookie                    |              list\[str\]               |                     抖音网页版Cookie，必需参数<br>可以使用 Cookie_tool.py 写入配置文件                      |
|                   dynamic                   |              list\[bool\]              |                                   是否下载动态封面图，默认值：False                                   |
|                  original                   |              list\[bool\]              |                                   是否下载静态封面图，默认值：False                                   |
|                   proxies                   |              list\[str\]               |                                   代理地址，设置为空字符串代表不使用代理                                   |
|                     log                     |                  bool                  |                                   是否记录运行日志，默认值：False                                    |

# 📄 配置文件示例

```json
{
  "accounts": [
    [
      "https://www.douyin.com/user/demo_1",
      "post",
      "2023/6/10",
      ""
    ],
    [
      "https://www.douyin.com/user/demo_2",
      "post",
      "2023/6/10",
      ""
    ]
  ],
  "music": [
    false,
    true
  ],
  "cookie": [
    "cookie_1",
    "cookie_2"
  ],
  "dynamic": [
    false,
    true
  ],
  "original": [
    false,
    false
  ],
  "proxies": [
    "",
    "http://127.0.0.1:9999"
  ]
}
```

**单线程模式：**
music、cookie、dynamic、original、proxies参数仅第一个值生效，下载多个账号的作品均使用`false(不下载音乐), cookie_1, false(不下载动态封面图), false(不下载静态封面图), ""(不使用代理)`
参数

**多线程模式：**
accounts、music、cookie、dynamic、original、proxies的元素个数必须相同，下载第一个账号的作品使用`false(不下载音乐), cookie_1, false(不下载动态封面图), false(不下载静态封面图), ""(不使用代理)`
参数，下载第二个账号的作品使用`true(下载音乐), cookie_2, true(下载动态封面图), false(不下载静态封面图), http://127.0.0.1:9999(使用代理)`
参数，每个账号按照索引对应的参数单独生效

**其余参数为全局参数**

# 💡 代码参考

* https://github.com/Johnserf-Seed/TikTokDownload
* https://github.com/Evil0ctal/Douyin_TikTok_Download_API
* https://requests.readthedocs.io/en/latest/
* https://dormousehole.readthedocs.io/en/latest/
* https://github.com/B1gM8c/X-Bogus
* https://html5up.net/
