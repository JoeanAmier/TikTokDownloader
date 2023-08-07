<div align="center">
<img src="https://github.com/JoeanAmier/TikTokDownloader/blob/master/static/images/TikTokDownloader.png" alt="TikTokDownloader" height="256" width="256"><br>
<h1>TikTokDownloader 文档</h1>
<a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/license">
<img src="https://img.shields.io/github/license/JoeanAmier/TikTokDownloader?color=f39800" alt="GNU General Public License v3.0">
</a>
<img src="https://img.shields.io/github/stars/JoeanAmier/TikTokDownloader?color=9ebc19" alt="stars">
<a href="https://sourcery.ai">
<img src="https://img.shields.io/badge/Sourcery-enabled-ffd900" alt="Sourcery">
</a>
<img src="https://img.shields.io/github/forks/JoeanAmier/TikTokDownloader?color=ba79b1" alt="forks">
<a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">
<img src="https://img.shields.io/github/v/release/JoeanAmier/TikTokDownloader?color=6f94cd" alt="TikTokDownloader">
</a>
</div>
<br>
<p>🔥 <b>TikTok 视频/图集/原声；抖音视频/图集/直播/原声/合集/评论/账号/搜索/热榜数据采集工具：</b>完全开源，基于 Requests 模块实现；批量下载抖音账号发布页或者喜欢页的作品；单独下载抖音链接或 TikTok 链接对应的作品；获取抖音直播推流地址；下载抖音直播视频；采集抖音作品评论数据；批量下载抖音合集作品；采集抖音账号详细数据；采集抖音用户 / 作品搜索结果；采集抖音热榜数据。</p>
<hr>
<h1>快速入门</h1>
<ol>
<li>安装不低于 <code>3.10</code> 版本的 <a href="https://www.python.org/">Python</a> 解释器</li>
<li>下载最新源码或 <a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">Releases</a> 发布的源码至本地</li>
<li>安装 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/requirements.txt">requirements.txt</a> 包含的第三方模块</li>
<li>运行 main.py</li>
<li>将 Cookie 信息写入配置文件
<ol><b>手动复制粘贴</b>
<li>使用浏览器打开抖音网页版，复制全部 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E6%95%99%E7%A8%8B.md">Cookie</a> 至剪贴板</li>
<li>选择 <code>复制粘贴写入 Cookie</code> 模式，按照提示将 Cookie 写入配置文件</li>
</ol>
<ol><b>扫码登录获取</b>
<li>选择 <code>扫码登陆写入 Cookie</code> 模式，程序会弹出登录二维码图片</li>
<li>使用抖音 APP 扫描二维码并登录账号，操作后关闭图片窗口</li>
<li>按照提示将 Cookie 写入配置文件</li>
</ol>
</li>
<li>返回程序界面，依次选择 <code>终端命令行模式</code> --> <code>单独下载链接作品</code></li>
<li>输入抖音或 TikTok 作品链接即可下载作品文件</li>
</ol>
<h1>基础说明</h1>
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
<td align="center">账号、视频、图集、直播、合集</td>
</tr>
<tr>
<td align="center"><code>https://vm.tiktok.com/分享码/</code></td>
<td align="center">视频、图集</td>
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
<td align="center"><code>https://www.tiktok.com/@账号昵称/video/作品ID</code></td>
<td align="center">账号、视频、图集</td>
</tr>
</tbody></table>
<ul>
<li>长链接：使用浏览器打开抖音或 TikTok 链接时，地址栏所显示的 URL 地址。</li>
<li>短链接：点击 APP 或网页版的分享按钮得到的 URL 地址，抖音平台以 <code>https://v.</code> 开头，掺杂中文和其他字符；TikTok
平台以 <code>https://vm</code> 开头，不掺杂其他字符；使用时不需要手动去除中文和其他字符，程序会自动提取 URL 链接。</li>
</ul>
<h2>数据储存</h2>
<ul>
<li><code>settings.json</code> 的 <code>save</code> 参数可设置数据储存格式类型。</li>
<li><code>采集作品评论数据</code>、<code>批量采集账号数据</code>、<code>采集搜索结果数据</code>、<code>采集抖音热榜数据</code> 模式必须设置 <code>save</code> 参数才能正常使用。</li>
<li>程序所有数据均储存至 <code>root</code> 参数路径下的 <code>Data</code> 文件夹。</li>
</ul>
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
<td align="center">单独下载链接作品</td>
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
</tbody></table>
<h1>配置文件</h1>
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
<td align="center">账号/合集标识, 设置为空字符串代表使用账号昵称/合集标题, <strong>属于 accounts 和 mix 子参数</strong></td>
</tr>
<tr>
<td align="center">url</td>
<td align="center">str</td>
<td align="center">账号主页/合集作品链接, 批量下载时使用<br><strong>属于 accounts 和 mix 子参数</strong></td>
</tr>
<tr>
<td align="center">mode</td>
<td align="center">str</td>
<td align="center">批量下载类型, <code>post</code> 代表发布页, <code>favorite</code> 代表喜欢页<br>需要账号喜欢页公开可见, <strong>属于 accounts 子参数</strong></td>
</tr>
<tr>
<td align="center">earliest</td>
<td align="center">str</td>
<td align="center">作品最早发布日期, 格式: <code>2023/1/1</code>, 设置为空字符串代表不限制, <strong>属于 accounts 子参数</strong></td>
</tr>
<tr>
<td align="center">latest</td>
<td align="center">str</td>
<td align="center">作品最晚发布日期, 格式: <code>2023/1/1</code>, 设置为空字符串代表不限制, <strong>属于 accounts 子参数</strong></td>
</tr>
<tr>
<td align="center">accounts[mark, url, mode, earliest, latest]</td>
<td align="center">list[list[str, str, str, str, str]]</td>
<td align="center">账号标识, 账号链接, 批量下载类型, 最早发布日期, 最晚发布日期; 批量下载账号作品时使用, 支持多账号, 以列表格式包含五个参数</td>
</tr>
<tr>
<td align="center">mix[mark, url]</td>
<td align="center">list[list[str, str]]</td>
<td align="center">合集标识, 合集链接或作品链接, 批量下载合集作品时使用<br>支持多合集, 以列表格式包含两个参数</td>
</tr>
<tr>
<td align="center">root</td>
<td align="center">str</td>
<td align="center">作品文件和数据记录保存路径, 默认值: 当前路径 <code>./</code></td>
</tr>
<tr>
<td align="center">folder</td>
<td align="center">str</td>
<td align="center">下载单独链接作品时, 储存文件夹的名称, 默认值: <code>Download</code></td>
</tr>
<tr>
<td align="center">name</td>
<td align="center">str</td>
<td align="center">文件保存时的命名规则, 值之间使用空格分隔<br>默认值: 发布时间-账号昵称-描述<br><code>id</code>: 唯一值, <code>desc</code>: 描述, <code>create_time</code>: 发布时间<br><code>nickname</code>: 账号昵称, <code>mark</code>: 账号标识, <code>uid</code>: 账号UID</td>
</tr>
<tr>
<td align="center">time</td>
<td align="center">str</td>
<td align="center">发布时间的格式, 默认值: <code>年-月-日 时.分.秒</code><br>注意: Windows 系统的文件名称不能包含英文冒号 <code>:</code></td>
</tr>
<tr>
<td align="center">split</td>
<td align="center">str</td>
<td align="center">文件命名的分隔符, 默认值: <code>-</code></td>
</tr>
<tr>
<td align="center">music</td>
<td align="center">bool</td>
<td align="center">是否下载作品音乐, 默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">save</td>
<td align="center">str</td>
<td align="center">采集数据持久化储存格式, 设置为空字符串代表不保存<br>支持: <code>csv</code>、<code>xlsx</code>、<code>sql</code>(SQLite)</td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">dict</td>
<td align="center">抖音网页版 Cookie, 必需参数; 使用 <code>main.py</code> 写入配置文件</td>
</tr>
<tr>
<td align="center">dynamic</td>
<td align="center">bool</td>
<td align="center">是否下载动态封面图, 默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">original</td>
<td align="center">bool</td>
<td align="center">是否下载静态封面图, 默认值: <code>false</code></td>
</tr>
<tr>
<td align="center">proxies</td>
<td align="center">str</td>
<td align="center">代理地址, 设置为空字符串代表不使用代理</td>
</tr>
<tr>
<td align="center">log</td>
<td align="center">bool</td>
<td align="center">是否记录运行日志, 默认值: <code>false</code></td>
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
<td align="center">每次从服务器接收的数据块大小, 单位字节; 默认值：<code>524288</code>(512 KB)</td>
</tr>
<tr>
<td align="center">retry</td>
<td align="center">int</td>
<td align="center">发送请求获取数据发生异常时重试的最大次数<br>设置为 <code>0</code> 代表关闭重试, 默认值: <code>10</code></td>
</tr>
<tr>
<td align="center">pages</td>
<td align="center">int</td>
<td align="center">批量下载账号喜欢页作品或者采集作品评论数据时<br>请求数据的最大次数，默认值: <code>0</code> 代表不限制</td>
</tr>
<tr>
<td align="center">thread</td>
<td align="center">bool</td>
<td align="center">是否启用多线程下载作品文件，默认值: <code>false</code></td>
</tr>
</tbody></table>
<h2>配置示例</h2>

```json
{
  "accounts": [
    [
      "账号标注1",
      "账号主页链接, 支持长链接与短链接",
      "post",
      "2023/7/1",
      ""
    ],
    [
      "账号标注2",
      "账号主页链接, 支持长链接与短链接",
      "favorite",
      "",
      "2023/8/1"
    ]
  ],
  "mix": [
    [
      "合集标识1",
      "https://www.douyin.com/collection/123, 支持合集链接与作品链接"
    ],
    [
      "合集标识2",
      "https://www.douyin.com/video/123, 支持长链接与短链接"
    ]
  ],
  "root": "./",
  "folder": "Download",
  "name": "create_time nickname id desc",
  "time": "%Y-%m-%d %H.%M.%S",
  "split": "-",
  "music": false,
  "save": "sql",
  "cookie": {
    "passport_csrf_token": "222",
    "passport_csrf_token_default": "222",
    "odin_tt": "222"
  },
  "dynamic": false,
  "original": false,
  "proxies": "http://127.0.0.1:9999",
  "log": false,
  "download": true,
  "max_size": 10485760,
  "chunk": 1048576,
  "retry": 20,
  "pages": 2,
  "thread": true
}
```

<p><strong>服务器部署模式：</strong> 仅 <code>cookie</code>、<code>proxies</code>、<code>retry</code> 参数生效，其余参数均不生效，但仍需正确编辑配置文件。</p>
<h2>参数详解</h2>

```json
{
  "root": "C:\\TikTokDownloader",
  "folder": "SOLO"
}
```

<p>代表程序会将下载的文件和记录的数据储存至 <code>C:\TikTokDownloader</code> 文件夹内，单独下载的作品文件会储存至 <code>C:\TikTokDownloader\SOLO</code> 文件夹内。</p>

```json
{
  "name": "create_time uid id",
  "split": " @ "
}
```

<p>代表作品文件名称格式为: <code>发布时间 @ 作者UID @ 作品ID</code></p>
<ul>
<li>如果作品没有描述，保存时文件名称的描述内容将替换为作品 ID</li>
<li>单独下载链接作品时，如果在 <code>name</code> 参数中设置了 <code>mark</code>，程序会自动替换为 <code>nickname</code></li>
</ul>

```json
{
  "time": "%Y-%m-%d"
}
```

<p>代表发布时间格式为：XXXX年-XX月-XX日，详细设置规则可以 <a href="https://docs.python.org/zh-cn/3/library/time.html?highlight=strftime#time.strftime">查看文档</a></p>

```json
{
  "save": "xlsx"
}
```

<p>代表使用 <code>XLSX</code> 格式储存程序采集数据。</p>

```json
{
  "max_size": 10485760
}
```

<p>代表作品文件大小限制为 10485760 字节(10 MB)，超过该大小的作品文件会自动跳过下载；直播文件不受限制。</p>

```json
{
  "chunk": 1048576
}
```

<p>代表下载文件时每次从服务器接收 1048576 字节 (1 MB)的数据块。</p>
<ul>
<li>影响下载速度：较大的 chunk 会增加每次下载的数据量，从而提高下载速度。相反，较小的 chunk 会降低每次下载的数据量，可能导致下载速度稍慢。</li>
<li>影响内存占用：较大的 chunk 会一次性加载更多的数据到内存中，可能导致内存占用增加。相反，较小的 chunk 会减少每次加载的数据量，从而降低内存占用。</li>
</ul>

```json
{
  "pages": 2
}
```

<p>代表批量下载账号喜欢页作品或者采集作品评论数据时，仅获取前 <code>2</code> 页数据；用于解决批量下载账号喜欢页作品需要获取全部数据的问题，以及作品评论数据数量过多的采集问题。</p>
<p>不影响批量下载账号发布页作品，如需控制账号发布页数据获取次数，可使用 <code>earliest</code> 和 <code>latest</code> 参数实现。</p>
<h1>功能介绍</h1>
<h2>复制粘贴写入 Cookie</h2>
<p>从浏览器复制全部 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E6%95%99%E7%A8%8B.md">Cookie</a>
至剪贴板，按照程序提示输入 Cookie 后回车确认，程序会自动提取并写入配置文件。</p>
<h2>扫码登陆写入 Cookie</h2>
<p>程序自动获取抖音登录二维码，并使用默认应用打开二维码图片，使用者通过抖音 APP 扫码并登录账号，操作后关闭二维码图片，程序会自动检查登录结果并将登陆后的 Cookie 写入配置文件。</p>
<h2>终端命令行模式</h2>
<p>功能最全面的模式，支持全部功能。</p>
<h3>批量下载账号作品</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接；此选项仅支持批量下载账号发布页作品，且不支持参数设置。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/user/账号ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>每个账号的作品会下载至 <code>root</code> 参数路径下的账号文件夹，账号文件夹格式为 <code>UID123456789_mark</code> 或者 <code>UID123456789_账号昵称</code></p>
<h3>单独下载链接作品</h3>
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
<p>作品会下载至 <code>root</code> 参数和 <code>folder</code> 参数拼接成的文件夹。</p>
<h3>获取直播推流地址</h3>
<p>输入直播链接，不支持已结束的直播。</p>
<p>支持链接格式：</p>
<ul>
<li><code>https://live.douyin.com/直播ID</code></li>
<li><code>https://v.douyin.com/分享码/</code></li>
</ul>
<p>下载说明：</p>
<ul>
<li>单次输入一个直播链接时，程序会询问用户是否下载直播视频，如果使用本程序下载，需要保持程序运行直到直播结束。</li>
<li>单次输入多个直播链接时，程序不会询问用户是否下载视频。</li>
<li>下载的直播视频时长会显示为直播总时长，实际视频内容是从下载时间开始，后面部分的片段无法播放。</li>
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
<p>支持采集评论回复、评论表情、评论图片；必须设置 <code>save</code> 参数才能正常使用。</p>
<p>储存名称格式：<code>作品123456789_评论数据</code></p>
<h3>批量下载合集作品</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>mix</code> 参数中的合集链接或作品链接。</li>
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
<p>每个合集的作品会下载至 <code>root</code> 参数路径下的合集文件夹，合集文件夹格式为 <code>MIX123456789_mark</code> 或者 <code>MIX123456789_合集标题</code></p>
<h3>批量采集账号数据</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/user/账号ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>重复获取相同账号数据时会储存为新的数据行，不会覆盖原有数据；必须设置 <code>save</code> 参数才能正常使用。</p>
<h3>采集搜索结果数据</h3>
<h4>输入格式</h4>
<p><strong>格式：</strong><code>关键词</code> <code>类型</code> <code>页数</code> <code>排序规则</code> <code>时间筛选</code></p>
<ul>
<li>搜索类型：<code>综合搜索</code> <code>视频搜索</code> <code>用户搜索</code></li>
<li>排序依据：<code>综合排序</code> <code>最新发布</code> <code>最多点赞</code></li>
<li>发布时间：<code>0</code>：不限；<code>1</code>：一天内；<code>7</code>：一周内；<code>182</code>：半年内</li>
</ul>
<p>参数之间使用空格分隔，<code>类型</code> 和 <code>排序规则</code> 支持输入中文或者对应索引，<code>页数</code> 和 <code>时间筛选</code> 仅支持输入整数。</p>
<p>程序采集的抖音搜索结果会储存至文件，储存名称格式：<code>搜索类型_排序依据_发布时间_关键词_时间戳</code>；不支持直接下载搜索结果作品；必须设置 <code>save</code> 参数才能正常使用。</p>
<h4>输入示例</h4>
<p><strong>输入：</strong><code>猫咪</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>综合搜索</code>；页数：<code>1</code>；排序依据：<code>综合排序</code>；发布时间：<code>不限</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 1 2 1</code> 等效于 <code>猫咪 视频搜索 2 最新发布</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>视频搜索</code>；页数：<code>2</code>；排序依据：<code>最新发布</code>；发布时间：<code>不限</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 0 10 0 7</code> 等效于 <code>猫咪 综合搜索 10 综合排序 7</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>综合搜索</code>；页数：<code>10</code>；排序依据：<code>综合排序</code>；发布时间：<code>一周内</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 1 5 2 182</code> 等效于 <code>猫咪 视频搜索 5 最多点赞 182</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>视频搜索</code>；页数：<code>5</code>；排序依据：<code>最多点赞</code>；发布时间：<code>半年内</code></p>
<hr>
<p><strong>输入：</strong><code>猫咪 2 2</code> 等效于 <code>猫咪 用户搜索 2</code></p>
<p><strong>含义：</strong> 关键词：<code>猫咪</code>；搜索类型：<code>用户搜索</code>；页数：<code>2</code></p>
<h3>采集抖音热榜数据</h3>
<p>采集 <code>热榜</code>、<code>娱乐榜</code>、<code>社会榜</code>、<code>挑战榜</code> 数据并储存至文件；必须设置 <code>save</code> 参数才能正常使用。</p>
<p>储存名称格式：<code>HOT_时间戳_热榜名称</code></p>
<h2>Web API 接口模式</h2>
<p>启动服务器，提供 API 调用服务，可以部署至私有服务器。</p>
<p><strong>未进行高并发测试，可能存在问题！</strong></p>
<p><strong>API 接口通用说明：</strong></p>
<ul>
<li>请求类型：<code>POST</code></li>
<li>请求格式：<code>JSON</code></li>
<li>响应格式：<code>JSON</code></li>
</ul>
<h3>配置文件修改接口</h3>
<p>修改 <code>settings.json</code> 配置文件；无需发送全部参数，仅发送想要修改的参数；参数格式与配置文件格式保持一致。</p>
<p>请求接口：<code>/init/</code></p>
<p>请求参数</p>

```json
{
  "root": "可选参数",
  "folder": "可选参数",
  "name": "可选参数",
  "time": "可选参数",
  "split": "可选参数",
  "music": "可选参数",
  "save": "可选参数",
  "cookie": "可选参数",
  "dynamic": "可选参数",
  "original": "可选参数",
  "proxies": "可选参数",
  "log": "可选参数",
  "max_size": "可选参数",
  "retry": "可选参数",
  "pages": "可选参数",
  "chunk": "可选参数"
}
```

<p>响应参数</p>

```json
{
  "message": "success"
}
```

<h3>账号作品数据接口</h3>
<p>返回账号发布页或者喜欢页的作品数据</p>
<p>请求接口：<code>/account/</code></p>
<p>请求参数</p>

```json
{
  "url": "账号主页链接，字符串，必需",
  "mode": "发布页或者喜欢页类型，字符串，可选",
  "earliest": "作品最早发布日期，字符串，可选",
  "latest": "作品最晚发布日期，字符串，可选",
  "pages": "账号喜欢页作品数据最大请求次数，整数，可选"
}
```

<p>响应参数</p>

```json
{
  "video": [
    "视频作品数据-1，JSON 格式",
    "视频作品数据-2，JSON 格式",
    "..."
  ],
  "image": [
    "图集作品数据-1，JSON 格式",
    "图集作品数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>链接作品数据接口</h3>
<p>返回作品详细数据；<strong>支持 TikTok 平台。</strong></p>
<p>请求接口：<code>/detail/</code></p>
<p>请求参数</p>

```json
{
  "url": "作品链接，字符串，必需"
}
```

<p>响应参数</p>

```json
{
  "detail": [
    "作品数据，JSON 格式"
  ],
  "message": "success"
}
```

<h3>直播推流数据接口</h3>
<p>返回直播推流数据</p>
<p>请求接口：<code>/live/</code></p>
<p>请求参数</p>

```json
{
  "url": "直播链接，字符串，必需"
}
```

<p>响应参数</p>

```json
{
  "live": [
    "直播数据，JSON 格式"
  ],
  "message": "success"
}
```

<h3>作品评论数据接口</h3>
<p>返回作品评论数据</p>
<p>请求接口：<code>/comment/</code></p>
<p>请求参数</p>

```json
{
  "url": "作品链接，字符串，必需",
  "pages": "作品评论数据最大请求次数，整数，可选"
}
```

<p>响应参数</p>

```json
{
  "comment": [
    "评论数据-1，JSON 格式",
    "评论数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>合集作品数据接口</h3>
<p>返回合集作品数据</p>
<p>请求接口：<code>/mix/</code></p>
<p>请求参数</p>

```json
{
  "url": "属于合集的作品链接，字符串，必需"
}
```

<p>响应参数</p>

```json
{
  "video": [
    "视频作品数据-1，JSON 格式",
    "视频作品数据-2，JSON 格式",
    "..."
  ],
  "image": [
    "图集作品数据-1，JSON 格式",
    "图集作品数据-2，JSON 格式",
    "..."
  ],
  "message": "success"
}
```

<h3>账号详细数据接口</h3>
<p>返回账号详细数据</p>
<p>请求接口：<code>/user/</code></p>
<p>请求参数</p>

```json
{
  "url": "账号主页链接，字符串，必需"
}
```

<p>响应参数</p>

```json
{
  "account": [
    "账号详细数据，JSON 格式"
  ],
  "message": "success"
}
```

<h2>Web UI 交互模式</h2>
<p>提供浏览器可视化交互界面，支持 <code>单独下载链接作品功能</code> 和 <code>获取直播推流地址功能</code>，支持局域网远程访问，可以部署至私有服务器，不可直接部署至公开服务器。</p>
<h2>服务器部署模式</h2>
<p>提供浏览器可视化交互界面，支持 <code>单独下载链接作品功能</code>，用于部署至公开服务器，为网站访客提供作品下载服务。</p>
<p>为保护访客隐私，<code>服务器部署模式</code> 禁用了日志记录和数据存储功能，不会记录任何作品提取数据。</p>
<h2>启用/禁用检查更新功能</h2>
<p>启用检查更新功能后，运行程序时会向 <code>https://github.com/JoeanAmier/TikTokDownloader/releases/latest</code>
发送请求获取最新 <code>Releases</code> 版本号，并提示是否存在新版本。</p>
<p>如果存在新版本会提示新版本的 <code>URL</code> 地址，不会自动下载更新。</p>
<h2>启用/禁用彩色交互提示</h2>
<p>程序支持终端彩色交互提示；如果终端不支持控制符，程序会直接输出代码，此时建议禁用彩色交互提示。</p>
<h2>启用/禁用作品下载记录</h2>
<p>用于解决下载作品文件后移动作品文件导致重复下载的问题！</p>
<ul>
<li>禁用该功能时，下载作品会检测作品文件是否存在，如果文件已存在将会跳过下载。</li>
<li>启用该功能时，下载作品会检测记录文件是否存在作品 ID，如果存在 ID 记录将会跳过下载(即使文件不存在)
，如果删除作品文件后想要重新下载，需要删除记录文件中的作品 ID 后重新运行。</li>
</ul>
<p>记录文件路径: <code>./cache/IDRecorder.txt</code></p>
<p><strong>不建议在程序运行过程中访问记录文件！</strong></p>
<h1>其他功能说明</h1>
<h2>单次输入多个链接</h2>
<p><code>单独下载链接作品</code>、<code>获取直播推流地址</code>、<code>采集作品评论数据</code>、<code>批量下载合集作品</code>、<code>批量采集账号数据</code>
支持单次输入多个链接，实现批量下载 / 提取功能；单次输入多个链接时，链接类型需要保持一致，不支持短链接与长链接混合输入。</p>
<h3>输入示例</h3>
<p><code>提取账号数据模式</code> 输入多个长链接时，需要使用空格分隔，其余模式不需要分隔字符，此处示例使用空格分隔仅仅便于观察区分链接。</p>
<p>无需对复制的链接进行处理，程序会自动提取输入文本中的有效链接。</p>
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
<li><code>name</code> 参数中没有使用 <code>nickname</code> 时，<code>mark</code> 设置没有限制。</li>
<li><code>name</code> 参数中使用了 <code>nickname</code> 时，<code>mark</code> 与 <code>nickname</code> 不能设置为包含关系的字符串。</li>
</ul>
<p><strong>示例：</strong></p>
<ul>
<li>✔️ <code>nickname</code>：ABC，<code>mark</code>：DEF</li>
<li>✔️ <code>nickname</code>：ABC，<code>mark</code>：BCD</li>
<li>❌ <code>nickname</code>：ABC，<code>mark</code>：AB</li>
<li>❌ <code>nickname</code>：BC，<code>mark</code>：ABC</li>
</ul>
<h3>账号标识说明</h3>
<ul>
<li>账号标识 <code>mark</code> 参数相当于账号备注，便于用户识别账号作品文件夹，避免账号昵称修改导致无法识别已下载作品问题。</li>
<li><code>批量下载账号作品</code> 模式下，如果设置了 <code>mark</code> 参数，下载的作品将会保存至 <code>UID123456789_mark参数</code>
或 <code>UID123456789_mark参数_喜欢页</code> 文件夹内。</li>
<li><code>批量下载账号作品</code> 模式下，如果 <code>mark</code>
参数设置为空字符串，程序将会使用账号昵称作为账号标识，下载的作品将会保存至 <code>UID123456789_账号昵称</code>
或 <code>UID123456789_账号昵称_喜欢页</code> 文件夹内。</li>
</ul>
<h3>合集标识说明</h3>
<p>与账号标识作用一致。</p>
<h3>如何修改标识</h3>
<p><strong>修改账号标识:</strong> 修改 <code>accounts</code> 的 <code>mark</code> 参数，再次运行 <code>批量下载账号作品</code> 模式，程序会自动应用新的账号标识。</p>
<p><strong>修改合集标识:</strong> 修改 <code>mix</code> 的 <code>mark</code> 参数，再次运行 <code>批量下载合集作品</code> 模式，程序会自动应用新的账号标识；或者手动输入合集链接，根据程序提示进行设置。</p>
<h3>账户昵称修改</h3>
<p>在 <code>批量下载账号作品</code> 和 <code>批量下载合集作品</code> 模式下，程序会判断账号昵称是否有修改，如果有修改，程序会自动识别已下载作品文件名称中的账户昵称，并修改至最新账户昵称。</p>
<h3>FileCache.json</h3>
<p><strong>缓存文件</strong>
用于记录账号 / 合集标识和账号昵称，当账号 / 合集标识或账号昵称发生变化时，程序会读取文件内容，并对相应的文件夹和文件进行重命名更新处理，如果该文件不存在或者删除该文件，程序首次运行不会判断账号 / 合集标识和账号昵称是否发生变化，程序运行结束后会生成新的缓存文件，之后程序才能监控账号 / 合集标识和账号昵称变化。</p>
<p><strong>缓存文件仅供程序读取和写入，不建议手动编辑文件内容。</strong></p>
<h1>服务器部署模式二次开发</h1>
<h2>API 文档</h2>
<p>请求URL：<code>/solo/</code></p>
<p>请求类型：<code>POST</code></p>
<p>请求格式：<code>JSON</code></p>
<p>请求参数：</p>

```json
{
  "url": "抖音作品链接或 TikTok 作品链接"
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
