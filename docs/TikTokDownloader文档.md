<div align="center">
<img src="https://github.com/JoeanAmier/TikTokDownloader/blob/master/static/images/TikTokDownloader.png" alt="TikTokDownloader" height="256" width="256"><br>
<h1>TikTokDownloader 文档</h1>
<img alt="GitHub" src="https://img.shields.io/github/license/JoeanAmier/TikTokDownloader?style=for-the-badge&color=ff7a45">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/JoeanAmier/TikTokDownloader?style=for-the-badge&color=fa8c16">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/JoeanAmier/TikTokDownloader?style=for-the-badge&color=ff4d4f">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/JoeanAmier/TikTokDownloader?style=for-the-badge&color=13c2c2">
<br>
<img alt="GitHub release (with filter)" src="https://img.shields.io/github/v/release/JoeanAmier/TikTokDownloader?style=for-the-badge&color=f759ab">
<img src="https://img.shields.io/badge/Sourcery-enabled-884898?style=for-the-badge&color=1890ff" alt="">
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/JoeanAmier/TikTokDownloader/total?style=for-the-badge&color=52c41a">
</div>
<br>
<p>🔥 <b>TikTok 主页/视频/图集/原声；抖音主页/视频/图集/收藏/直播/原声/合集/评论/账号/搜索/热榜数据采集工具：</b>完全开源，基于 Requests 模块实现的免费工具；批量下载抖音账号发布、喜欢、收藏作品；批量下载 TikTok 账号主页作品；下载抖音链接或 TikTok 链接作品；获取抖音直播推流地址；下载抖音直播视频；采集抖音作品评论数据；批量下载抖音合集作品；采集抖音账号详细数据；采集抖音用户 / 作品 / 直播搜索结果；采集抖音热榜数据。</p>
<p>⭐ <b>项目文档正在完善中，如有发现任何错误或描述模糊之处，请告知作者以便改进！</b></p>
<hr>
<h1>快速入门</h1>
<ol>
<li><b>下载 EXE 程序</b> 或者 <b>配置运行环境</b>
<ol><b>直接运行程序</b>
<li>下载 <a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">Releases</a> 发布的 EXE 程序压缩包</li>
<li>解压后打开程序文件夹，双击运行 <code>main.exe</code></li>
</ol>
<ol><b>通过源码运行</b>
<li>安装不低于 <code>3.12</code> 版本的 <a href="https://www.python.org/">Python</a> 解释器</li>
<li>下载最新的源码或 <a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">Releases</a> 发布的源码至本地</li>
<li>运行 <code>python -m venv venv</code> 命令创建虚拟环境（可选）</li>
<li>运行 <code>.\venv\Scripts\activate.ps1</code> 或者 <code>venv\Scripts\activate</code> 命令激活虚拟环境（可选）</li>
<li>运行 <code>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt</code> 命令安装程序所需模块</li>
<li>运行 <code>python .\main.py</code> 或者 <code>python main.py</code> 命令启动 TikTokDownloader</li>
</ol>
</li>
<li>阅读 TikTokDownloader 的免责声明，根据提示输入内容</li>
<li>将 Cookie 信息写入配置文件
<ol><b>手动复制粘贴(推荐)</b>
<li>参考 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E6%95%99%E7%A8%8B.md">Cookie 提取教程</a>，复制所需 Cookie 至剪贴板</li>
<li>选择 <code>复制粘贴写入 Cookie</code> 选项，按照提示将 Cookie 写入配置文件</li>
</ol>
<ol><b>扫码登录获取</b>
<li>选择 <code>扫码登陆写入 Cookie</code> 选项，程序会显示登录二维码图片，并使用默认应用打开图片</li>
<li>使用抖音 APP 扫描二维码并登录账号</li>
<li>按照提示操作，将 Cookie 写入配置文件</li>
</ol>
</li>
<li>返回程序界面，依次选择 <code>终端命令行模式</code> -> <code>批量下载链接作品</code></li>
<li>输入抖音或 TikTok 作品链接即可下载作品文件</li>
</ol>
<h1>获取 Cookie</h1>
<p><a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E6%95%99%E7%A8%8B.md">点击查看 Cookie 获取教程</a>，无效的 Cookie 会导致程序获取数据失败或者无法下载高分辨率视频文件；目前尚无检查 Cookie 有效性的方法。</p>
<h1>入门说明</h1>
<h2>关于终端</h2>
<p>⭐ 推荐使用 <a href="https://learn.microsoft.com/zh-cn/windows/terminal/install">Windows 终端</a>（Windows 11 自带默认终端）运行程序以便获得最佳彩色交互显示效果！</p>
<h2>链接类型</h2>
<table>
<thead>
<tr>
<th align="center">链接格式</th>
<th align="center">链接内容</th>
</tr>
</thead>
<tbody><tr>
<td align="center"><code>https://v.douyin.com/分享码/</code></td>
<td align="center">账号、视频、图集、直播、合集、话题</td>
</tr>
<tr>
<td align="center"><code>https://vm.tiktok.com/分享码/</code></td>
<td align="center">账号、视频、图集</td>
</tr>
<tr>
<td align="center"><code>https://www.douyin.com/note/作品ID</code></td>
<td align="center">图集</td>
</tr>
<tr>
<td align="center"><code>https://www.douyin.com/video/作品ID</code></td>
<td align="center">视频</td>
</tr>
<tr>
<td align="center"><code>https://www.douyin.com/collection/合集ID</code></td>
<td align="center">合集</td>
</tr>
<tr>
<td align="center"><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></td>
<td align="center">账号、视频、图集</td>
</tr>
<tr>
<td align="center"><code>https://live.douyin.com/直播ID</code></td>
<td align="center">直播</td>
</tr>
<tr>
<td align="center"><code>https://www.tiktok.com/@TikTok号/video/作品ID</code></td>
<td align="center">账号、视频、图集</td>
</tr>
</tbody></table>
<ul>
<li>账号/作品/直播完整链接：使用浏览器打开抖音或 TikTok 链接时，地址栏所显示的 URL 地址。</li>
<li>分享链接：点击 APP 或网页版的分享按钮得到的 URL 地址，抖音平台以 <code>https://v.</code> 开头，掺杂中文和其他字符；TikTok
平台以 <code>https://vm</code> 开头，不掺杂其他字符；使用时不需要手动去除中文和其他字符，程序会自动提取 URL 链接。</li>
</ul>
<h2>数据储存</h2>
<ul>
<li>配置文件 <code>settings.json</code> 的 <code>storage_format</code> 参数可设置数据储存格式类型，如果不设置该参数，程序不会储存任何数据至文件。</li>
<li><code>采集作品评论数据</code>、<code>批量采集账号数据</code>、<code>采集搜索结果数据</code>、<code>采集抖音热榜数据</code> 模式必须设置 <code>storage_format</code> 参数才能正常使用。</li>
<li>程序所有数据均储存至 <code>root</code> 参数路径下的 <code>Data</code> 文件夹。</li>
</ul>
<h2>直播下载</h2>
<p><code>获取直播推流地址</code> 功能支持调用 <code>ffmpeg</code> 下载直播，程序会优先调用系统环境的 <code>ffmpeg</code>，其次调用 <code>ffmpeg</code> 参数指定的 <code>ffmpeg</code>，如果 <code>ffmpeg</code> 不可用，程序将会调用内置下载器下载直播。</p>
<p>建议配置 <code>ffmpeg</code> 环境，<code>ffmpeg.exe</code> 可前往 <a href="http://ffmpeg.org/download.html">官方网站</a> 获取。</p>
<h2>功能简介</h2>
<table>
<thead>
<tr>
<th align="center">程序功能</th>
<th align="center">功能类型</th>
</tr>
</thead>
<tbody><tr>
<td align="center">批量下载账号作品</td>
<td align="center">文件下载, 数据采集</td>
</tr>
<tr>
<td align="center">批量下载链接作品</td>
<td align="center">文件下载, 数据采集</td>
</tr>
<tr>
<td align="center">获取直播推流地址</td>
<td align="center">文件下载, 数据提取</td>
</tr>
<tr>
<td align="center">采集作品评论数据</td>
<td align="center">数据采集</td>
</tr>
<tr>
<td align="center">批量下载合集作品</td>
<td align="center">文件下载, 数据采集</td>
</tr>
<tr>
<td align="center">批量采集账号数据</td>
<td align="center">数据采集</td>
</tr>
<tr>
<td align="center">采集搜索结果数据</td>
<td align="center">数据采集</td>
</tr>
<tr>
<td align="center">采集抖音热榜数据</td>
<td align="center">数据采集</td>
</tr>
<tr>
<td align="center">批量下载收藏作品</td>
<td align="center">文件下载，数据采集</td>
</tr>
</tbody></table>
<h1>配置文件</h1>
<p>配置文件：项目根目录下的 <code>settings.json</code> 文件，可以自定义设置程序部分运行参数。</p>
<p><b><code>cookie</code> 参数为必需参数，必须设置该参数才能正常使用程序</b>；其余参数可以根据实际需求进行修改！</p>
<p>如果您的计算机没有合适的程序编辑 JSON 文件，建议使用 <a href="https://try8.cn/tool/format/json">JSON 在线工具</a> 编辑配置文件内容。</p>
<p>注意: 手动修改 <code>settings.json</code> 后需要重新运行程序才会生效！</p>
<h2>参数含义</h2>
<table>
<thead>
<tr>
<th align="center">参数</th>
<th align="center">类型</th>
<th align="center">说明</th>
</tr>
</thead>
<tbody><tr>
<td align="center">mark</td>
<td align="center">str</td>
<td align="center">账号/合集标识, 设置为空字符串代表使用账号昵称/合集标题, <strong>属于 accounts_urls、mix_urls 和 owner_url 子参数</strong></td>
</tr>
<tr>
<td align="center">url</td>
<td align="center">str</td>
<td align="center">账号主页/合集作品链接, 批量下载时使用<br><strong>属于 accounts_urls、mix_urls 和 owner_url 子参数</strong></td>
</tr>
<tr>
<td align="center">tab</td>
<td align="center">str</td>
<td align="center">批量下载类型, <code>post</code> 代表发布作品, <code>favorite</code> 代表喜欢作品<br>需要账号喜欢作品公开可见, <strong>属于 Accounts_Urls 子参数</strong></td>
</tr>
<tr>
<td align="center">earliest</td>
<td align="center">str</td>
<td align="center">作品最早发布日期, 格式: <code>2023/1/1</code>, 设置为空字符串代表不限制, <strong>属于 accounts_urls 子参数</strong></td>
</tr>
<tr>
<td align="center">latest</td>
<td align="center">str</td>
<td align="center">作品最晚发布日期, 格式: <code>2023/1/1</code>, 设置为空字符串代表不限制, <strong>属于 accounts_urls 子参数</strong></td>
</tr>
<tr>
<td align="center">accounts_urls[mark, url, tab, earliest, latest]</td>
<td align="center">list[dict[str, str, str, str, str]]</td>
<td align="center">账号标识, 账号链接, 批量下载类型, 最早发布日期, 最晚发布日期; 批量下载账号作品时使用, 支持多账号, 以字典格式包含五个参数</td>
</tr>
<tr>
<td align="center">mix_urls[mark, url]</td>
<td align="center">list[dict[str, str]]</td>
<td align="center">合集标识, 合集链接或作品链接, 批量下载合集作品时使用<br>支持多合集, 以字典格式包含两个参数</td>
</tr>
<tr>
<td align="center">owner_url[mark, url]</td>
<td align="center">dict[str, str]</td>
<td align="center">已登录 Cookie 的账号标识, 账号主页链接, 批量下载收藏作品时使用<br>用于获取账号昵称和 UID, 以字典格式包含两个参数</td>
</tr>
<tr>
<td align="center">root</td>
<td align="center">str</td>
<td align="center">作品文件和数据记录保存路径, 建议使用绝对路径，默认值: <code>项目根路径</code></td>
</tr>
<tr>
<td align="center">folder_name</td>
<td align="center">str</td>
<td align="center">下载单独链接作品时, 保存文件夹的名称, 默认值: <code>Download</code></td>
</tr>
<tr>
<td align="center">name_format</td>
<td align="center">str</td>
<td align="center">文件保存时的命名规则, 值之间使用空格分隔<br>默认值: 发布时间-作品类型-账号昵称-描述<br><code>id</code>: 作品 ID, <code>desc</code>: 作品描述, <code>create_time</code>: 发布时间<br><code>nickname</code>: 账号昵称, <code>mark</code>: 账号标识, <code>uid</code>: 账号 ID, <code>type</code>: 作品类型</td>
</tr>
<tr>
<td align="center">date_format</td>
<td align="center">str</td>
<td align="center">日期时间格式, 默认值: <code>年-月-日 时:分:秒</code></td>
</tr>
<tr>
<td align="center">split</td>
<td align="center">str</td>
<td align="center">文件命名的分隔符, 默认值: <code>-</code></td>
</tr>
<tr>
<td align="center">folder_mode</td>
<td align="center">bool</td>
<td align="center">是否将每个作品的文件储存至单独的文件夹，文件夹名称格式与 <code>name_format</code> 参数保持一致，默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">music</td>
<td align="center">bool</td>
<td align="center">是否下载作品音乐, 默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">storage_format</td>
<td align="center">str</td>
<td align="center">采集数据持久化储存格式, 设置为空字符串代表不保存<br>支持: <code>csv</code>、<code>xlsx</code>、<code>sql</code>(SQLite)</td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">dict | str</td>
<td align="center">抖音网页版 Cookie, 必需参数; 建议通过程序写入配置文件，亦可手动编辑</td>
</tr>
<tr>
<td align="center">dynamic_cover</td>
<td align="center">bool</td>
<td align="center">是否下载动态封面图, 默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">original_cover</td>
<td align="center">bool</td>
<td align="center">是否下载静态封面图, 默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">proxies</td>
<td align="center">str</td>
<td align="center">代理地址, 设置为空字符串代表不使用代理</td>
</tr>
<tr>
<td align="center">download</td>
<td align="center">bool</td>
<td align="center">是否打开下载功能, 如果关闭, 程序将不会下载任何文件; 默认值: <code>true</code></td>
</tr>
<tr>
<td align="center">max_size</td>
<td align="center">int</td>
<td align="center">作品文件大小限制, 单位字节, 超出大小限制的作品文件将会跳过下载<br>设置为 <code>0</code> 代表无限制</td>
</tr>
<tr>
<td align="center">chunk</td>
<td align="center">int</td>
<td align="center">每次从服务器接收的数据块大小, 单位字节; 默认值：<code>1048576</code>(1 MB)</td>
</tr>
<tr>
<td align="center">max_retry</td>
<td align="center">int</td>
<td align="center">发送请求获取数据发生异常时重试的最大次数<br>设置为 <code>0</code> 代表关闭重试, 默认值: <code>10</code></td>
</tr>
<tr>
<td align="center">max_pages</td>
<td align="center">int</td>
<td align="center">批量下载账号喜欢作品、收藏作品或者采集作品评论数据时<br>请求数据的最大次数（不包括异常重试），默认值: <code>0</code> 代表不限制</td>
</tr>
<tr>
<td align="center">default_mode</td>
<td align="center">int</td>
<td align="center">程序启动的默认模式</td>
</tr>
<tr>
<td align="center">ffmpeg</td>
<td align="center">str</td>
<td align="center"><code>ffmpeg.exe</code> 路径，下载直播时使用，如果系统环境存在 <code>ffmpeg</code> 或者不想使用 <code>ffmpeg</code>，可以不设置该参数</td>
</tr>
</tbody></table>
<h2>配置示例</h2>

```json
{
  "accounts_urls": [
    {
      "mark": "账号标识-1",
      "url": "账号主页链接-1",
      "tab": "post",
      "earliest": "2023/1/1",
      "latest": "2023/6/1"
    },
    {
      "mark": "",
      "url": "账号主页链接-2",
      "tab": "favorite",
      "earliest": "2023/7/1",
      "latest": ""
    }
  ],
  "mix_urls": [
    {
      "mark": "",
      "url": "合集链接或者作品链接"
    },
    {
      "mark": "合集标识-2",
      "url": "合集链接或者作品链接"
    }
  ],
  "owner_url": {
    "mark": "已登录 Cookie 的账号标识，可以设置为空字符串（可选）",
    "url": "已登录 Cookie 的账号主页链接（可选）"
  },
  "root": "C:\\TikTokDownloader",
  "folder_name": "SOLO",
  "name_format": "create_time uid id",
  "date_format": "%Y-%m-%d",
  "split": " @ ",
  "folder_mode": false,
  "music": false,
  "storage_format": "xlsx",
  "cookie": {
    "passport_csrf_token": "demo",
    "passport_csrf_token_default": "demo",
    "odin_tt": "demo"
  },
  "dynamic_cover": false,
  "original_cover": false,
  "proxies": "http://127.0.0.1:9999",
  "download": true,
  "max_size": 104857600,
  "chunk": 10485760,
  "max_retry": 10,
  "max_pages": 2,
  "default_mode": 3,
  "ffmpeg": "C:\\TikTokDownloader\\ffmpeg.exe"
}
```

<p><strong>服务器部署模式：</strong> 仅 <code>cookie</code>、<code>proxies</code>、<code>max_retry</code> 参数生效，其余参数均不生效，但仍需正确编辑配置文件。</p>
<h2>参数详解</h2>
<h3>下载喜欢作品</h3>

```json
{
  "accounts_urls": [
    {
      "mark": "",
      "url": "账号主页链接-1",
      "tab": "favorite",
      "earliest": "",
      "latest": ""
    },
    {
      "mark": "",
      "url": "账号主页链接-2",
      "tab": "post",
      "earliest": "",
      "latest": ""
    },
    {
      "mark": "",
      "url": "账号主页链接-3",
      "tab": "favorite",
      "earliest": "",
      "latest": ""
    }
  ]
}
```

<p>将待下载的账号信息写入配置文件，每个账号对应一个对象/字典，<code>tab</code> 参数设置为 <code>favorite</code> 代表批量下载喜欢作品，支持多账号。</p>
<p><b>批量下载账号喜欢作品需要使用已登录的 Cookie，否则可能无法获取正确的账号信息！</b></p>
<h3>发布日期限制</h3>

```json
{
  "accounts_urls": [
    {
      "mark": "账号标识",
      "url": "账号主页链接",
      "tab": "post",
      "earliest": "2023/12/1",
      "latest": ""
    }
  ]
}
```

<p>如果已经采集某账号的全部发布作品，建议设置 <code>earliest</code> 和 <code>latest</code> 参数以减少后续采集请求次数。</p>
<p>例如：将 <code>earliest</code> 参数设置为 <code>2023/12/1</code>，程序获取账号发布作品数据时，无需获取早于 <code>2023/12/1</code> 的作品数据，可减少请求次数提高运行效率。</p>
<h3>文件储存路径</h3>

```json
{
  "root": "C:\\TikTokDownloader",
  "folder_name": "SOLO"
}
```

<p>代表程序会将下载的文件和记录的数据储存至 <code>C:\TikTokDownloader</code> 文件夹内，链接下载的作品文件会储存至 <code>C:\TikTokDownloader\SOLO</code> 文件夹内。</p>
<h3>文件名称格式</h3>

```json
{
  "name_format": "create_time uid id",
  "split": " @ "
}
```

<p>代表作品文件名称格式为: <code>发布时间 @ 作者UID @ 作品ID</code></p>
<ul>
<li>如果作品没有描述，保存时文件名称的描述内容将替换为作品 ID</li>
<li>批量下载链接作品时，如果在 <code>name_format</code> 参数中设置了 <code>mark</code> 字段，程序会自动替换为 <code>nickname</code> 字段</li>
</ul>
<h3>日期时间格式</h3>

```json
{
  "date_format": "%Y-%m-%d"
}
```

<p>代表发布时间格式为：XXXX年-XX月-XX日，详细设置规则可以 <a href="https://docs.python.org/zh-cn/3/library/time.html?highlight=strftime#time.strftime">查看文档</a></p>
<h3>数据储存格式</h3>

```json
{
  "storage_format": "xlsx"
}
```

<p>代表使用 <code>XLSX</code> 格式储存程序采集数据。</p>
<h3>文件大小限制</h3>

```json
{
  "max_size": 104857600
}
```

<p>代表作品文件大小限制为 104857600 字节(100 MB)，超过该大小的作品文件会自动跳过下载；直播文件不受限制。</p>
<h3>文件分块下载</h3>

```json
{
  "chunk": 10485760
}
```

<p>代表下载文件时每次从服务器接收 10485760 字节 (10 MB)的数据块。</p>
<ul>
<li>影响下载速度：较大的 chunk 会增加每次下载的数据量，从而提高下载速度。相反，较小的 chunk 会降低每次下载的数据量，可能导致下载速度稍慢。</li>
<li>影响内存占用：较大的 chunk 会一次性加载更多的数据到内存中，可能导致内存占用增加。相反，较小的 chunk 会减少每次加载的数据量，从而降低内存占用。</li>
</ul>
<h3>请求次数限制</h3>

```json
{
  "max_pages": 2
}
```

<p>代表批量下载账号喜欢作品、收藏作品或者采集作品评论数据时，仅获取前 <code>2</code> 页数据；用于解决批量下载账号喜欢作品、收藏作品需要获取全部数据的问题，以及作品评论数据数量过多的采集问题。</p>
<p>不影响批量下载账号发布作品，如需控制账号发布作品数据获取次数，可使用 <code>earliest</code> 和 <code>latest</code> 参数实现。</p>
<h3>默认启动模式</h3>

```json
{
  "default_mode": 3
}
```

<p>代表运行程序自动进入 <code>终端命令行模式</code>，其他示例：<code>4</code> 代表 <code>Web API 接口模式</code>，<code>5</code> 代表 <code>Web UI 交互模式</code>，<code>6</code> 代表 <code>服务器部署模式</code>。</p>
<h3>程序代理设置</h3>

```json
{
  "proxies": "http://127.0.0.1:9999"
}
```

<p>代表程序获取网络数据时使用 <code>http://127.0.0.1:9999</code> 作为代理；程序会自动验证代理是否可用，如果代理不可用，则 <code>proxies</code> 参数不生效。</p>
<p>如果您的电脑使用了代理工具且未修改默认端口，可以尝试以下设置：</p>
<ul>
<li>Clash: <code>http://127.0.0.1:7890</code></li>
<li>v2rayN: <code>http://127.0.0.1:10809</code></li>
</ul>

<h1>高级配置</h1>
<p>如果想要进一步修改程序功能，可以编辑 <code>src/Customizer.py</code> 文件（不适用于 EXE 程序），按照注释指引和实际需求进行自定义修改。</p>
<b>部分可自定义设置的功能：</b>
<ul>
<li>设置作品文件下载的最大线程数量</li>
<li>设置文件名称的作品描述长度限制</li>
<li>设置非法字符替换规则</li>
<li>开启服务器模式局域网访问功能</li>
<li>设置服务器模式主机及端口</li>
<li>设置 Cookie 更新间隔</li>
<li>设置彩色交互提示颜色</li>
<li>设置请求数据时间间隔</li>
<li>设置作品下载记录数据备份间隔</li>
<li>设置获取数据失败时的处理策略</li>
<li>设置自定义作品筛选规则</li>
<li>设置分批获取数据策略</li>
<li>设置服务器模式参数验证</li>
</ul>
<h1>功能介绍</h1>
<h2>复制粘贴写入 Cookie</h2>
<p>参考 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E6%95%99%E7%A8%8B.md">Cookie 提取教程</a>，手动从浏览器复制所需 Cookie 至剪贴板，按照程序提示输入 Cookie 后回车确认，程序会自动处理 Cookie 并写入配置文件。</p>
<p><b>推荐使用该方法获取 Cookie</b>，如果粘贴 Cookie 至终端后无响应，可能是 Cookie 文本长度超出终端最大文本长度限制，请考虑更换终端或者其他写入方式。</p>
<h2>扫码登录写入 Cookie</h2>
<p>程序自动获取抖音登录二维码，随后会在终端输出二维码，并使用系统默认图片浏览器打开二维码图片，使用者通过抖音 APP 扫码并登录账号，操作后关闭二维码图片窗口，程序会自动检查登录结果并将登录后的 Cookie 写入配置文件。</p>
<p><b>注意：</b>扫码登录获取的 Cookie 有效期更短，且频繁扫码登录容易导致账号被风控！</p>
<h2>终端命令行模式</h2>
<p>功能最全面的模式，支持全部功能。</p>
<h3>批量下载账号作品(TikTok)</h3>
<p><b>注意：该模式为半自动模式，需要手动将 TikTok 账号主页保存为 HTML 文件后再使用本工具批量下载！</b></p>
<p>支持输入格式：</p>
<ol>
<li>单账号：单个 HTML 文件路径</li>
<li>多账号：包含 HTML 文件的文件夹路径</li>
</ol>
<p>如果仅需下载单个账号的发布/喜欢作品，只需输入对应的 HTML 文件路径；如果需要下载多个账号的发布/喜欢作品，可以将全部 HTML 文件放置在同一文件夹内，输入文件夹路径进行处理；每个账号的作品会下载至 <code>root</code> 参数路径下的账号文件夹，账号文件夹格式为 <code>UID123456789_账号昵称_类型</code></p>
<p><b>HTML 文件获取教程</b></p>
<ol>
<li>使用浏览器打开待采集的 TikTok 账号主页页面</li>
<li>向下滚动页面，直至所有作品完全加载</li>
<li>按下 <code>F12</code> 打开 <code>开发人员工具</code> 窗口</li>
<li>切换到 <code>控制台</code> 选项卡</li>
<li>输入以下命令，按下回车键
<pre>
// 获取网页标题
const title = document.title;

// 创建一个新的 Blob 对象，用于保存 HTML 内容
const blob = new Blob([document.documentElement.outerHTML], {type: 'text/html'});

// 创建一个下载链接元素
const downloadLink = document.createElement('a');

// 将网页标题作为文件名
downloadLink.download = title + '.html';

// 设置下载链接的属性
downloadLink.href = URL.createObjectURL(blob);

// 将下载链接添加到页面中并模拟点击下载
document.body.appendChild(downloadLink);
downloadLink.click();

// 清理下载链接元素
document.body.removeChild(downloadLink);
</pre>
</li>
<li>浏览器会弹出下载窗口，下载文件即可</li>
</ol>
<h3>批量下载账号作品(抖音)</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts_urls</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接；此选项仅支持批量下载账号发布页作品，暂不支持参数设置。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/user/账号ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>如果需要大批量采集账号作品，建议启用 <code>src/Customizer.py</code> 文件的 <code>suspend</code> 函数。</p>
<p>如果当前账号昵称或账号标识不是有效的文件夹名称时，程序会提示用户输入临时的账号标识，以便程序继续处理账号。</p>
<p>处理多个账号时，如果某个账号获取数据失败，程序会询问用户是否继续处理（可编辑 <code>src/Customizer.py</code> 文件修改功能）</p>
<p>每个账号的作品会下载至 <code>root</code> 参数路径下的账号文件夹，账号文件夹格式为 <code>UID123456789_mark_类型</code> 或者 <code>UID123456789_账号昵称_类型</code></p>
<h3>批量下载链接作品</h3>
<p>输入作品链接；<strong>支持 TikTok 平台。</strong></p>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://vm.tiktok.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
<li><code>https://www.tiktok.com/@账号昵称/video/作品ID</code></li>
</ul>
<p>作品会下载至 <code>root</code> 参数和 <code>folder_name</code> 参数拼接成的文件夹。</p>
<h3>获取直播推流地址</h3>
<p>输入直播链接，不支持已结束的直播。</p>
<p>支持链接格式：</p>
<ul>
<li><code>https://live.douyin.com/直播ID</code></li>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/follow?webRid=直播ID</code></li>
</ul>
<p>下载说明：</p>
<ul>
<li>程序会询问用户是否下载直播视频，支持同时下载多个直播视频。</li>
<li>程序调用 <code>ffmpeg</code> 下载直播时，关闭 TikTokDownloader 不会影响直播下载。</li>
<li>程序调用内置下载器下载直播时，需要保持 TikTokDownloader 运行直到直播结束。</li>
<li>程序询问是否下载直播时，输入直播清晰度或者对应序号即可下载，例如：下载最高清晰度输入 <code>FULL_HD1</code> 或者 <code>1</code> 均可。</li>
<li>程序调用内置下载器下载的直播文件，视频时长会显示为直播总时长，实际视频内容从下载时间开始，靠后部分的片段无法播放。</li>
<li>直播视频会下载至 <code>root</code> 参数路径下的 <code>Live</code> 文件夹</li>
</ul>
<h3>采集作品评论数据</h3>
<p>输入作品链接。</p>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>支持采集评论回复、评论表情、评论图片；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<p>储存名称格式：<code>作品123456789_评论数据</code></p>
<h3>批量下载合集作品</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>mix_urls</code> 参数中的合集链接或作品链接。</li>
<li>输入合集链接，或者属于合集的任意一个作品链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/collection/合集ID</code></li>
</ul>
<p>如果需要大批量采集合集作品，建议启用 <code>src/Customizer.py</code> 文件的 <code>suspend</code> 函数。</p>
<p>如果当前合集标题或合集标识不是有效的文件夹名称时，程序会提示用户输入临时的合集标识，以便程序继续处理合集。</p>
<p>处理多个合集时，如果某个合集获取数据失败，程序会询问用户是否继续处理（可编辑 <code>src/Customizer.py</code> 文件修改功能）</p>
<p>每个合集的作品会下载至 <code>root</code> 参数路径下的合集文件夹，合集文件夹格式为 <code>MIX123456789_mark_合集作品</code> 或者 <code>MIX123456789_合集标题_合集作品</code></p>
<h3>批量采集账号数据</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts_urls</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/user/账号ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>重复获取相同账号数据时会储存为新的数据行，不会覆盖原有数据；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<h3>采集搜索结果数据</h3>
<h4>搜索条件输入格式</h4>
<p><strong>格式：</strong><code>关键词</code> <code>搜索类型</code> <code>页数</code> <code>排序规则</code> <code>时间筛选</code></p>
<ul>
<li>搜索类型：<code>综合搜索</code> <code>视频搜索</code> <code>用户搜索</code> <code>直播搜索</code>（可省略 “ 搜索 ” 字符）</li>
<li>排序依据：<code>综合排序</code> <code>最多点赞</code> <code>最新发布</code></li>
<li>时间筛选：<code>0</code>：不限；<code>1</code>：一天内；<code>7</code>：一周内；<code>182</code>：半年内</li>
</ul>
<p>参数之间使用空格分隔，<code>搜索类型</code> 和 <code>排序规则</code> 支持输入中文或者对应索引，<code>页数</code> 和 <code>时间筛选</code> 仅支持输入整数。</p>
<p>程序采集的抖音搜索结果会储存至文件，储存名称格式：<code>搜索数据_搜索时间_搜索类型_关键词_排序依据_时间筛选</code>；不支持直接下载搜索结果作品；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<p><code>用户搜索</code> 和 <code>直播搜索</code> 不需要输入排序依据和时间筛选！</p>
<h4>输入示例</h4>
<p><strong>输入：</strong><code>猫咪</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>综合搜索</code>；页数：<code>1</code>；排序依据：<code>综合排序</code>；时间筛选：<code>不限</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 1 2 1</code> 等效于 <code>猫咪 视频搜索 2 最多点赞</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>视频搜索</code>；页数：<code>2</code>；排序依据：<code>最多点赞</code>；时间筛选：<code>不限</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 0 10 0 7</code> 等效于 <code>猫咪 综合搜索 10 综合排序 7</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>综合搜索</code>；页数：<code>10</code>；排序依据：<code>综合排序</code>；时间筛选：<code>一周内</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 1 5 2 182</code> 等效于 <code>猫咪 视频搜索 5 最新发布 182</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>视频搜索</code>；页数：<code>5</code>；排序依据：<code>最新发布</code>；时间筛选：<code>半年内</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 2 2</code> 等效于 <code>猫咪 用户搜索 2</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>用户搜索</code>；页数：<code>2</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 3 2</code> 等效于 <code>猫咪 直播搜索 2</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>直播搜索</code>；页数：<code>2</code></p>
<h3>采集抖音热榜数据</h3>
<p>无需输入，采集 <code>抖音热榜</code>、<code>娱乐榜</code>、<code>社会榜</code>、<code>挑战榜</code> 数据并储存至文件；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<p>储存名称格式：<code>实时热榜数据_采集时间_热榜名称</code></p>
<h3>批量下载收藏作品</h3>
<p>无需输入，需要在配置文件写入已登录的 Cookie，并在 <code>owner_url</code> 参数填入对应的账号主页链接和账号标识（可选）；目前仅支持采集当前 Cookie 对应账号的收藏作品。</p>
<p>如果未设置 <code>owner_url</code> 参数，程序会使用临时字符串作为账号昵称和 UID。</p>
<p>账号文件夹格式为 <code>UID123456789_mark_收藏作品</code> 或者 <code>UID123456789_账号昵称_收藏作品</code></p>
<h2>Web API 接口模式</h2>
<p>启动服务器，提供 API 调用功能；支持局域网远程访问，可以部署至私有服务器或者公开服务器，远程部署建议设置参数验证。</p>
<p>默认禁用局域网访问，如需开启，请修改 <code>src/Customizer.py</code> 文件的 <code>SERVER_HOST</code> 变量。</p>
<p>部分接口支持传入临时 <code>cookie</code> 参数，如果传入临时 <code>cookie</code> 参数，本次 API 请求会使用临时 <code>cookie</code> 向抖音服务器获取数据，如果没有传入 <code>cookie</code> 参数，程序会使用配置文件的 <code>cookie</code> 参数；需要注意临时 <code>cookie</code> 和配置文件 <code>cookie</code> 参数的有效性；程序不会储存临时 <code>cookie</code> 内容。</p>
<p>目前支持调用 API 获取数据，暂不支持调用 API 下载文件！</p>
<p><strong>API 接口通用说明：</strong></p>
<ul>
<li>请求类型：<code>POST</code></li>
<li>请求格式：<code>JSON</code></li>
<li>响应格式：<code>JSON</code></li>
</ul>
<p><b>代码示例：</b></p>

```python
import requests

params = {
    "url": "https://www.douyin.com/note/12345678910",
    "source": True
}
response = requests.post("http://localhost:5000/detail/", json=params)
print(response.json())
```

<h3>配置文件修改接口</h3>
<p>修改 <code>settings.json</code> 配置文件；无需发送全部参数，仅需发送想要修改的参数；参数格式要求与配置文件格式要求保持一致。</p>
<p><b>请求接口：</b><code>/settings/</code></p>
<p><b>请求参数(可选)</b></p>

```json
{
  "root": "可选参数",
  "folder_name": "可选参数",
  "name_format": "可选参数",
  "date_format": "可选参数",
  "split": "可选参数",
  "folder_mode": "可选参数",
  "music": "可选参数",
  "storage_format": "可选参数",
  "cookie": "可选参数",
  "dynamic_cover": "可选参数",
  "original_cover": "可选参数",
  "proxies": "可选参数",
  "download": "可选参数",
  "max_size": "可选参数",
  "chunk": "可选参数",
  "max_retry": "可选参数",
  "max_pages": "可选参数",
  "default_mode": "可选参数",
  "ffmpeg": "可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>
<p>返回 <code>settings.json</code> 配置文件所有参数</p>
<h3>账号作品数据接口</h3>
<p>获取账号发布作品或者喜欢作品数据</p>
<p><b>请求接口：</b><code>/account/</code></p>
<p><b>请求参数</b></p>

```json
{
  "url": "账号主页链接，字符串，必需参数",
  "tab": "发布作品或者喜欢作品，字符串，可选参数，默认值: post",
  "earliest": "作品最早发布日期，字符串，可选参数",
  "latest": "作品最晚发布日期，字符串，可选参数",
  "pages": "账号喜欢作品数据最大请求次数，整数，可选参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "作品数据-1，JSON 格式",
    "作品数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>链接作品数据接口</h3>
<p>获取作品详细数据；<strong>支持 TikTok 平台。</strong></p>
<p><b>请求接口：</b><code>/detail/</code></p>
<p><b>请求参数</b></p>

```json
{
  "url": "作品链接，支持多作品，字符串，必需参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "作品数据-1，JSON 格式",
    "作品数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>直播推流数据接口</h3>
<p>获取直播推流数据</p>
<p><b>请求接口：</b><code>/live/</code></p>
<p><b>请求参数</b></p>

```json
{
  "url": "直播链接，支持多直播，字符串，必需参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "直播数据-1，JSON 格式",
    "直播数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>作品评论数据接口</h3>
<p>获取作品评论数据</p>
<p><b>请求接口：</b><code>/comment/</code></p>
<p><b>请求参数</b></p>

```json
{
  "url": "作品链接，字符串，必需参数",
  "pages": "作品评论数据最大请求次数，整数，可选参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "评论数据-1，JSON 格式",
    "评论数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>合集作品数据接口</h3>
<p>获取合集作品数据</p>
<p><b>请求接口：</b><code>/mix/</code></p>
<p><b>请求参数</b></p>

```json
{
  "url": "属于合集的作品链接，字符串，必需参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "作品数据-1，JSON 格式",
    "作品数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>账号详细数据接口</h3>
<p>获取账号详细数据</p>
<p><b>请求接口：</b><code>/user/</code></p>
<p><b>请求参数</b></p>

```json
{
  "url": "账号主页链接，支持多账号，字符串，必需参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "账号详细数据-1，JSON 格式",
    "账号详细数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>搜索结果数据接口</h3>
<p>获取抖音搜索结果数据</p>
<p><b>请求接口：</b><code>/search/</code></p>
<p><b>请求参数</b></p>

```json
{
  "keyword": "关键词，字符串，必需参数",
  "type": "搜索类型，字符串，可选参数",
  "pages": "结果页数，字符串，可选参数",
  "sort_type": "排序依据，字符串，可选参数",
  "publish_time": "发布时间，字符串，可选参数",
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "cookie": "抖音 cookie，字符串，可选参数",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "data": [
    "搜索结果数据-1，JSON 格式",
    "搜索结果数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>抖音热榜数据接口</h3>
<p>获取抖音热榜数据</p>
<p><b>请求接口：</b><code>/hot/</code></p>
<p><b>请求参数</b></p>

```json
{
  "source": "是否返回原始数据，布尔值，可选参数，默认值: false",
  "token": "自定义参数"
}
```

<p><b>响应参数</b></p>

```json
{
  "time": "热榜采集时间",
  "data": [
    {
      "抖音热榜": [
        "热榜数据-1，JSON 格式",
        "热榜数据-2，JSON 格式",
        "..."
      ]
    },
    {
      "娱乐榜": [
        "热榜数据-1，JSON 格式",
        "热榜数据-2，JSON 格式",
        "..."
      ]
    },
    {
      "社会榜": [
        "热榜数据-1，JSON 格式",
        "热榜数据-2，JSON 格式",
        "..."
      ]
    },
    {
      "挑战榜": [
        "热榜数据-1，JSON 格式",
        "热榜数据-2，JSON 格式",
        "..."
      ]
    }
  ],
  "message": "success"
}
```

<h2>Web UI 交互模式</h2>
<p>提供浏览器可视化交互界面，支持 <code>批量下载链接作品</code> 和 <code>获取直播推流地址</code> 功能，支持局域网远程访问，可以部署至私有服务器，不可直接部署至公开服务器。</p>
<h2>服务器部署模式</h2>
<p>提供浏览器可视化交互界面，支持 <code>批量下载链接作品</code> 功能，默认启用局域网访问，用于部署至公开服务器，为网站访客提供作品下载服务，建议设置参数验证。</p>
<p>支持远程修改 <code>settings.json</code> 配置文件，请参考 <code>配置文件修改接口</code></p>
<h2>启用/禁用检查更新功能</h2>
<p>启用检查更新功能后，运行程序时会向 <code>https://github.com/JoeanAmier/TikTokDownloader/releases/latest</code>
发送请求获取最新 <code>Releases</code> 版本号，并提示是否存在新版本。</p>
<p>如果检查新版本失败，可能是访问 GitHub 超时，并非功能异常；如果存在新版本会提示新版本的 <code>URL</code> 地址，不会自动下载更新。</p>
<h2>启用/禁用作品下载记录</h2>
<ul>
<li>启用该功能：程序会记录下载成功的作品 ID，如果对作品文件进行移动、重命名或者删除操作，程序不会重复下载该作品，如果想要重新下载该作品，需要删除记录文件中对应的作品 ID 后保存文件并重新运行程序。</li>
<li>禁用该功能：程序会在下载文件前检测文件是否存在，如果文件存在会自动跳过下载该作品，如果对作品文件进行移动、重命名或者删除操作，程序将会重新下载该作品。</li>
</ul>
<p>程序会周期性备份作品下载记录数据，当作品下载记录数据丢失时，程序会尝试通过备份文件恢复数据，备份周期可以通过 <code>src/Customizer.py</code> 文件设置。</p>
<p>记录文件路径: <code>./cache/IDRecorder.txt</code></p>
<p><strong>不建议在程序运行过程中访问记录文件！</strong></p>
<h2>启用/禁用运行日志记录</h2>
<p>是否将程序运行日志记录保存到文件，默认关闭，日志文件保存路径：<code>./Log</code></p>
<p>如果在使用过程中发现程序 Bug，可以及时告知作者，并附上日志文件，日志记录有助于作者分析 Bug 原因和修复 Bug。</p>
<h1>其他功能说明</h1>
<h2>单次输入多个链接</h2>
<p><code>批量下载账号作品</code>、<code>批量下载链接作品</code>、<code>获取直播推流地址</code>、<code>采集作品评论数据</code>、<code>批量下载合集作品</code>、<code>批量采集账号数据</code>
功能支持单次输入多个链接，实现批量下载 / 提取功能；单次输入多个链接时，链接类型需要保持一致，不支持完整链接与分享链接混合输入。</p>
<h3>输入示例</h3>
<p>输入多个链接时，需要使用空格分隔；无需对复制的链接进行额外处理，程序会自动提取输入文本中的有效链接。</p>
<ul>
<li>支持：<code>https://v.douyin.com/abc/</code> <code>https://v.douyin.com/abc/</code></li>
<li>支持：<code>https://www.douyin.com/video/123456789</code> <code>https://www.douyin.com/note/123456789</code></li>
<li>支持：<code>https://www.douyin.com/collection/123456789</code> <code>https://www.douyin.com/collection/123456789</code></li>
<li>支持：<code>https://www.douyin.com/user/ABC?modal_id=123456789</code> <code>https://www.douyin.com/note/123456789</code></li>
<li>不支持：<code>https://v.douyin.com/abc/</code> <code>https://www.douyin.com/video/123456789</code></li>
<li>不支持：<code>https://www.douyin.com/collection/123456789</code> <code>https://www.douyin.com/video/123456789</code></li>
<li>不支持：<code>https://www.douyin.com/video/123456789</code> <code>https://www.tiktok.com/@ABC/video/123456789</code></li>
</ul>
<h2>账号/合集标识</h2>
<h3>标识设置规则</h3>
<ul>
<li><code>name_format</code> 参数中没有使用 <code>nickname</code> 时，<code>mark</code> 设置没有限制。</li>
<li><code>name_format</code> 参数中使用了 <code>nickname</code> 时，<code>mark</code> 与 <code>nickname</code> 不能设置为包含关系的字符串。</li>
</ul>
<p><strong>标识示例：</strong></p>
<ul>
<li>✔️ <code>nickname</code>：ABC，<code>mark</code>：DEF</li>
<li>✔️ <code>nickname</code>：ABC，<code>mark</code>：BCD</li>
<li>❌ <code>nickname</code>：ABC，<code>mark</code>：AB</li>
<li>❌ <code>nickname</code>：BC，<code>mark</code>：ABC</li>
</ul>
<h3>账号标识说明</h3>
<ul>
<li>账号标识 <code>mark</code> 参数相当于账号备注，便于用户识别账号作品文件夹，避免账号昵称修改导致无法识别已下载作品问题。</li>
<li><code>批量下载账号作品</code> 模式下，如果设置了 <code>mark</code> 参数，下载的作品将会保存至 <code>UID123456789_mark_发布作品</code>
或 <code>UID123456789_mark_喜欢作品</code> 文件夹内。</li>
<li><code>批量下载账号作品</code> 模式下，如果 <code>mark</code>
参数设置为空字符串，程序将会使用账号昵称作为账号标识，下载的作品将会保存至 <code>UID123456789_账号昵称_发布作品</code>
或 <code>UID123456789_账号昵称_喜欢作品</code> 文件夹内。</li>
</ul>
<h3>合集标识说明</h3>
<p>与账号标识作用一致。</p>
<h3>如何修改标识</h3>
<p><strong>修改账号标识:</strong> 修改 <code>accounts_urls</code> 的 <code>mark</code> 参数，再次运行 <code>批量下载账号作品</code> 模式，程序会自动应用新的账号标识。</p>
<p><strong>修改合集标识:</strong> 修改 <code>mix_urls</code> 的 <code>mark</code> 参数，再次运行 <code>批量下载合集作品</code> 模式，程序会自动应用新的账号标识。</p>
<h3>账户昵称修改</h3>
<p>在 <code>批量下载账号作品</code> 和 <code>批量下载合集作品</code> 模式下，程序会判断账号昵称是否有修改，如果有修改，程序会自动识别已下载作品文件名称中的账户昵称，并修改至最新账户昵称。</p>
<h3>AccountCache.json</h3>
<p><strong>缓存文件</strong>
用于记录账号 / 合集标识和账号昵称，当账号 / 合集标识或账号昵称发生变化时，程序会读取文件内容，并对相应的文件夹和文件进行重命名更新处理，如果该文件不存在或者删除该文件，程序首次运行不会判断账号 / 合集标识和账号昵称是否发生变化，程序运行结束后会生成新的缓存文件，之后程序才能监控账号 / 合集标识和账号昵称变化。</p>
<p><strong>缓存文件仅供程序读取和写入，不建议手动编辑文件内容。</strong></p>
<h1>服务器部署模式二次开发</h1>
<h2>API 文档</h2>
<p>请求URL：<code>/single/</code></p>
<p>请求类型：<code>POST</code></p>
<p>请求格式：<code>JSON</code></p>
<p>请求参数：</p>

```json
{
  "url": "抖音作品链接或 TikTok 作品链接",
  "token": "自定义参数"
}
```

<p><strong>后端会自动处理 <code>url</code> 参数中的作品链接，可以不在前端对 <code>url</code> 参数进行额外处理。</strong></p>
<p>支持链接：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://vm.tiktok.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
<li><code>https://www.tiktok.com/@账号昵称/video/作品ID</code></li>
</ul>
<p>响应格式：<code>JSON</code></p>
<p>响应参数：</p>

```json
{
  "text": "解析结果提示, 字符串",
  "author": "作者昵称, 字符串; 失败时返回 null",
  "describe": "作品描述, 字符串; 失败时返回 null",
  "download": "作品下载地址, 视频返回字符串, 图集返回由下载地址成的数组; 失败时返回 false",
  "music": "原声下载地址, 字符串, 失败时返回 false",
  "origin": "静态封面图地址, 字符串; 失败时返回 false",
  "dynamic": "动态封面图地址, 字符串; 失败时返回 false",
  "preview": "作品预览图地址, 字符串, 视频返回静态封面图, 图集返回首张图片; 失败时返回空白预览图地址"
}
```

<h1>免责声明</h1>
<ul>
<li>使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。</li>
<li>本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者尽力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。</li>
<li>使用者在使用本项目时必须严格遵守 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/license">GNU
    General Public License v3.0</a> 的要求，并在适当的地方注明使用了 <a
        href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/license">GNU General Public License
    v3.0</a> 的代码。
</li>
<li>使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。</li>
<li>使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。</li>
<li>本项目的作者不会提供 TikTokDownloader 项目的付费版本，也不会提供与 TikTokDownloader 项目相关的任何商业服务。</li>
<li>基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各种情况负全部责任。</li>
</ul>
<b>在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。</b>
