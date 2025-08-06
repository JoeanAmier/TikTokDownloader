<div align="center">
<img src="https://github.com/JoeanAmier/TikTokDownloader/blob/master/static/images/DouK-Downloader.png" alt="DouK-Downloader" height="256" width="256"><br>
<h1>DouK-Downloader 项目文档</h1>
<a href="https://trendshift.io/repositories/6222" target="_blank"><img src="https://trendshift.io/api/badge/repositories/6222" alt="" style="width: 250px; height: 55px;" width="250" height="55"/></a>
<br>
<img alt="GitHub" src="https://img.shields.io/github/license/JoeanAmier/TikTokDownloader?style=flat-square">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/JoeanAmier/TikTokDownloader?style=flat-square&color=55efc4">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/JoeanAmier/TikTokDownloader?style=flat-square&color=fda7df">
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/JoeanAmier/TikTokDownloader?style=flat-square&color=a29bfe">
<br>
<img alt="Static Badge" src="https://img.shields.io/badge/Python-3.12-b8e994?style=flat-square&logo=python&labelColor=3dc1d3">
<img alt="GitHub release (with filter)" src="https://img.shields.io/github/v/release/JoeanAmier/TikTokDownloader?style=flat-square&color=48dbfb">
<img src="https://img.shields.io/badge/Sourcery-enabled-884898?style=flat-square&color=1890ff" alt="">
<img alt="Static Badge" src="https://img.shields.io/badge/Docker-badc58?style=flat-square&logo=docker">
<img alt="GitHub all releases" src="https://img.shields.io/github/downloads/JoeanAmier/TikTokDownloader/total?style=flat-square&color=ffdd59">
</div>
<br>
<p>🔥 <b>TikTok 发布/喜欢/合辑/直播/视频/图集/音乐；抖音发布/喜欢/收藏/收藏夹/视频/图集/实况/直播/音乐/合集/评论/账号/搜索/热榜数据采集工具：</b>完全开源，基于 HTTPX 模块实现的免费数据采集和文件下载工具；批量下载抖音账号发布、喜欢、收藏、收藏夹作品；批量下载 TikTok 账号发布、喜欢作品；下载抖音链接或 TikTok 链接作品；获取抖音直播推流地址；下载抖音直播视频；获取 TikTok 直播推流地址；下载 TikTok 直播视频；采集抖音作品评论数据；批量下载抖音合集作品；批量下载 TikTok 合辑作品；采集抖音账号详细数据；采集抖音用户 / 作品 / 直播搜索结果；采集抖音热榜数据。</p>
<p>⭐ <b>项目版本：<code>5.7 Beta</code>；更新日期：<code>2025/8/5</code></b></p>
<p>⭐ <b>项目文档正在完善，如果发现任何错误或描述模糊之处，请告知作者以便改进！本项目历史名称：<code>TikTokDownloader</code></b></p>
<hr>
<h1>快速入门</h1>
<p>⭐ 本项目包含手动构建可执行文件的 GitHub Actions，使用者可以随时使用 GitHub Actions 将最新源码构建为可执行文件！</p>
<p>⭐ 自动构建可执行文件教程请查阅本文档的 <code>构建可执行文件指南</code> 部分；如果需要更加详细的图文教程，请 <a href="https://mp.weixin.qq.com/s/TorfoZKkf4-x8IBNLImNuw">查阅文章</a>！</p>
<ol>
<li><b>运行可执行文件</b> 或者 <b>配置环境运行</b>
<ol><b>运行可执行文件</b>
<li>下载 <a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">Releases</a> 或者 Actions 构建的可执行文件压缩包</li>
<li>解压后打开程序文件夹，双击运行 <code>main</code></li>
</ol>
<ol><b>配置环境运行</b>

[//]: # (<li>安装不低于 <code>3.12</code> 版本的 <a href="https://www.python.org/">Python</a> 解释器</li>)
<li>安装 <code>3.12</code> 版本的 <a href="https://www.python.org/">Python</a> 解释器</li>
<li>下载最新的源码或 <a href="https://github.com/JoeanAmier/TikTokDownloader/releases/latest">Releases</a> 发布的源码至本地</li>
<li>运行 <code>python -m venv venv</code> 命令创建虚拟环境（可选）</li>
<li>运行 <code>.\venv\Scripts\activate.ps1</code> 或者 <code>venv\Scripts\activate</code> 命令激活虚拟环境（可选）</li>
<li>运行 <code>pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt</code> 命令安装程序所需模块</li>
<li>运行 <code>python .\main.py</code> 或者 <code>python main.py</code> 命令启动 DouK-Downloader</li>
</ol>
</li>
<li>阅读 DouK-Downloader 的免责声明，根据提示输入内容</li>
<li>将 Cookie 信息写入配置文件
<ol><b>从剪贴板读取 Cookie</b>
<li>参考 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6%95%99%E7%A8%8B.md">Cookie 提取教程</a>，复制所需 Cookie 至剪贴板</li>
<li>选择 <code>从剪贴板读取 Cookie</code> 选项，程序会自动读取剪贴板的 Cookie 并写入配置文件</li>
</ol>
<ol><b>从浏览器读取 Cookie</b>
<li>选择 <code>从浏览器读取 Cookie</code> 选项，按照提示输入浏览器类型或序号</li>
</ol>
<ol><b><del>扫码登录获取 Cookie</del>（失效）</b>
<li><del>选择 <code>扫码登录获取 Cookie</code> 选项，程序会显示登录二维码图片，并使用默认应用打开图片</del></li>
<li><del>使用抖音 APP 扫描二维码并登录账号</del></li>
<li><del>按照提示操作，程序会自动将 Cookie 写入配置文件</del></li>
</ol>
</li>
<li>返回程序界面，依次选择 <code>终端交互模式</code> -> <code>批量下载链接作品(抖音)</code> -> <code>手动输入待采集的作品链接</code></li>
<li>输入抖音作品链接即可下载作品文件</li>
</ol>
<p><b>TikTok 平台功能需要额外设置配置文件 <code>browser_info_tiktok</code> 的 <code>device_id</code> 参数，否则 TikTok 平台功能可能无法正常使用！参数获取方式与 Cookie 类似，详见 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6%95%99%E7%A8%8B.md">Cookie 获取教程</a></b></p>
<h2>Docker 容器</h2>
<ol>
<li>获取镜像</li>
<ul>
<li>方式一：使用 <code>Dockerfile</code> 文件构建镜像</li>
<li>方式二：使用 <code>docker pull joeanamier/tiktok-downloader</code> 命令拉取镜像</li>
<li>方式三：使用 <code>docker pull ghcr.io/joeanamier/tiktok-downloader</code> 命令拉取镜像</li>
</ul>
<li>创建容器：<code>docker run --name 容器名称(可选) -p 主机端口号:5555 -v tiktok_downloader_volume:/app/Volume -it &lt;镜像名称&gt;</code>
</li>
<br><b>注意：</b>此处的 <code>&lt;镜像名称&gt;</code> 需与您在第一步中使用的镜像名称保持一致（例如 <code>joeanamier/tiktok-downloader</code> 或 <code>ghcr.io/joeanamier/tiktok-downloader</code>）
<li>运行容器
<ul>
<li>启动容器：<code>docker start -i 容器名称/容器 ID</code></li>
<li>重启容器：<code>docker restart -i 容器名称/容器 ID</code></li>
</ul>
</li>
</ol>
<p>Docker 容器无法直接访问宿主机的文件系统，部分功能不可用，例如：<code>从浏览器读取 Cookie</code>；其他功能如有异常请反馈！</p>
<h1>Cookie 说明</h1>
<p><a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6%95%99%E7%A8%8B.md">点击查看 Cookie 获取教程</a>；无效或失效的 Cookie 会导致程序获取数据失败！</p>
<ul>
<li>Cookie 仅需在失效后重新写入配置文件，并非每次运行程序都要写入配置文件！</li>
<li><p>Cookie 会影响下载的视频文件分辨率，如果无法下载最高分辨率的视频文件，请尝试更新 Cookie！</li>
<li>程序获取数据失败时，可以尝试更新 Cookie 或者使用已登录的 Cookie！</li>
</ul>
<h1>入门说明</h1>
<h2>关于终端</h2>
<p>⭐ 推荐使用 <a href="https://learn.microsoft.com/zh-cn/windows/terminal/install">Windows 终端</a>（Windows 11 自带默认终端）运行程序以便获得最佳彩色交互显示效果！</p>
<h2>链接类型</h2>
<ul>
<li>完整链接：使用浏览器打开抖音或 TikTok 链接时，地址栏所显示的 URL 地址。</li>
<li>分享链接：点击 APP 或网页版的分享按钮得到的 URL 地址，抖音平台以 <code>https://v.</code> 开头，掺杂中文和其他字符；TikTok
平台以 <code>https://vm.</code> 或 <code>https://vt.</code> 开头，不掺杂其他字符；使用时<b>不需要</b>手动去除中文和其他字符，程序会自动提取 URL 链接。</li>
</ul>
<h2>数据储存</h2>
<ul>
<li>项目支持使用 <code>CSV</code>、<code>XLSX</code>、<code>SQLite</code> 格式文件储存采集数据。</li>
<li>配置文件 <code>settings.json</code> 的 <code>storage_format</code> 参数可设置数据储存格式类型，如果不设置该参数，程序不会储存任何数据至文件。</li>
<li><code>采集作品评论数据</code>、<code>采集账号详细数据</code>、<code>采集搜索结果数据</code>、<code>采集抖音热榜数据</code> 模式必须设置 <code>storage_format</code> 参数才能正常使用。</li>
<li>程序所有数据均储存至配置文件 <code>root</code> 参数路径下的 <code>Data</code> 文件夹。</li>
</ul>
<h2>文本文档</h2>
<p>项目部分功能支持从文本文档（TXT）读取链接，如需使用，请在计算机任意路径创建一个空白文本文档，然后编辑文件内容，每行输入单个链接，编辑完成后保存文件。</p>
<p>文本文档编码：UTF-8</p>
<h3>文本文档内容示例</h3>

```text
https://www.douyin.com/user/abcd?vid=123456789
https://www.douyin.com/search/key?modal_id=123456789
https://www.douyin.com/video/123456789
https://www.douyin.com/note/123456789
```

<h2>直播下载</h2>
<p><code>获取直播推流地址</code> 功能需要调用 <code>ffmpeg</code> 下载直播文件；程序会优先调用系统环境的 <code>ffmpeg</code>，其次调用 <code>ffmpeg</code> 参数指定的 <code>ffmpeg</code>，如果 <code>ffmpeg</code> 不可用，程序将不支持直播下载！</p>
<p>建议前往 <a href="https://ffmpeg.org/download.html">官方网站</a> 或者 <a href="https://github.com/BtbN/FFmpeg-Builds">FFmpeg-Builds</a> 获取 <code>ffmpeg</code> 程序！</p>
<p>项目开发时所用的 FFmpeg 版本信息如下，不同版本的 FFmpeg 可能会有差异；若功能异常，请向作者反馈！</p>
<pre>
ffmpeg version n7.1.1-6-g48c0f071d4-20250405 Copyright (c) 2000-2025 the FFmpeg developers
built with gcc 14.2.0 (crosstool-NG 1.27.0.18_7458341)
</pre>
<h2>功能汇总</h2>
<table>
<thead>
<tr>
<th align="center">程序功能</th>
<th align="center">功能类型</th>
</tr>
</thead>
<tbody><tr>
<td align="center">批量下载账号作品（发布、喜欢）</td>
<td align="center">文件下载, 数据采集</td>
</tr>
<tr>
<td align="center">批量下载链接作品</td>
<td align="center">文件下载, 数据采集</td>
</tr>
<tr>
<td align="center">获取直播推流地址</td>
<td align="center">文件下载, 数据采集</td>
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
<td align="center">采集账号详细数据</td>
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
<tr>
<td align="center">批量下载收藏夹作品</td>
<td align="center">文件下载，数据采集</td>
</tr>
<tr>
<td align="center">批量下载收藏音乐作品</td>
<td align="center">文件下载，数据采集</td>
</tr>
</tbody></table>
<h2>关闭平台功能</h2>
<p>本项目支持抖音平台和 TikTok 平台的数据采集和文件下载功能，平台功能默认开启，如果不需要使用平台的任何功能，可以编辑配置文件关闭平台功能。</p>
<p><del>本项目内置参数更新机制，程序会周期性更新抖音与 TikTok 请求的部分参数，以保持参数的有效性（或许没有效果？），该功能无法防止参数失效，参数失效后需要重新写入 Cookie；关闭平台功能后，对应平台的参数更新功能将会禁用！</del></p>
<h1>配置文件</h1>
<p>配置文件：项目根目录下的 <code>./Volume/settings.json</code> 文件，可以自定义设置程序部分运行参数。</p>
<p>若无特殊需求，大部分配置参数无需修改，直接使用默认值即可。</p>
<p><b><code>cookie</code>、<code>cookie_tiktok</code> 与 <code>device_id</code>参数为必需参数，必须设置该参数才能正常使用程序</b>；其余参数可以根据实际需求进行修改！</p>
<p>如果您的计算机没有合适的程序编辑 JSON 文件，建议使用 <a href="https://try8.cn/tool/format/json">JSON 在线工具</a> 编辑配置文件内容。</p>
<p>注意: 手动修改 <code>settings.json</code> 后需要重新运行程序才会生效！</p>
<h2>参数说明</h2>
<table>
<thead>
<tr>
<th align="center">参数</th>
<th align="center">类型</th>
<th align="center">说明</th>
<th align="center">默认</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><i>mark</i></td>
<td align="center">str</td>
<td align="center"><a href="#mark"><sup>1</sup></a>账号/合集标识，用于区分账号/合集；<strong>属于 accounts_urls、mix_urls 和 owner_url 子参数</strong></td>
<td align="center">账号昵称/合集标题</td>
</tr>
<tr>
<td align="center"><i>url</i></td>
<td align="center">str</td>
<td align="center">账号主页/合集作品链接；<strong>属于 accounts_urls、mix_urls 和 owner_url 子参数</strong></td>
<td align="center">无</td>
</tr>
<tr>
<td align="center"><i>tab</i></td>
<td align="center">str</td>
<td align="center"><a href="#supplement"><sup>2</sup></a>主页标签，<code>post</code> 代表发布作品、<code>favorite</code> 代表喜欢作品；<strong>属于 accounts_urls 子参数</strong></td>
<td align="center">发布作品</td>
</tr>
<tr>
<td align="center"><i>earliest</i></td>
<td align="center">str | float | int</td>
<td align="center">作品最早发布日期，格式：<code>2023/1/1</code>、<code>整数</code>、<code>浮点数</code>；设置为数值代表基于 <code>latest</code>参数的前 XX 天，<strong>属于 accounts_urls 子参数</strong></td>
<td align="center">不限制</td>
</tr>
<tr>
<td align="center"><i>latest</i></td>
<td align="center">str | float | int</td>
<td align="center">作品最晚发布日期，格式：<code>2023/1/1</code>、<code>整数</code>、<code>浮点数</code>；设置为数值代表基于当天的前 XX 天，<strong>属于 accounts_urls 子参数</strong></td>
<td align="center">不限制</td>
</tr>
<tr>
<td align="center"><i>enable</i></td>
<td align="center">bool</td>
<td align="center">参数对象是否启用，设置为 <code>false</code> 时程序会跳过处理；<strong>属于 accounts_urls 和 mix_urls 子参数</strong></td>
<td align="center">启用</td>
</tr>
<tr>
<td align="center">accounts_urls[mark, url, tab, earliest, latest, enable]</td>
<td align="center">list[dict[str, str, str, Any, str, bool]]</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>抖音平台：账号标识，账号链接，主页标签，最早发布日期，最晚发布日期，是否启用；作为 <code>批量下载账号作品</code> 模式选项，支持多账号，以字典格式包含六个参数</td>
<td align="center">无</td>
<tr>
<td align="center">mix_urls[mark, url, enable]</td>
<td align="center">list[dict[str, str, bool]]</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>抖音平台：合集标识，合集链接或作品链接，是否启用；作为 <code>批量下载合集作品</code> 模式选项，支持多合集，以字典格式包含三个参数</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">owner_url[mark, url]</td>
<td align="center">dict[str, str]</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>抖音平台：当前登录 Cookie 的账号标识，账号主页链接；<code>批量下载收藏作品</code> 模式下用于获取账号信息，以字典格式包含两个参数</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">accounts_urls_tiktok[mark, url, tab, earliest, latest, enable]</td>
<td align="center">list[dict[str, str, str, Any, str, bool]]</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>TikTok 平台；参数规则与 <code>accounts_urls</code> 一致</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">mix_urls_tiktok[mark, url, enable]</td>
<td align="center">list[dict[str, str, bool]]</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>TikTok 平台；参数规则与 <code>mix_urls</code> 一致</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">owner_url_tiktok[mark, url](未生效)</td>
<td align="center">dict[str, str]</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>TikTok 平台；参数规则与 <code>owner_url</code> 一致</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">root</td>
<td align="center">str</td>
<td align="center">作品文件和数据记录保存路径；建议使用绝对路径</td>
<td align="center">项目根路径/Volume</td>
</tr>
<tr>
<td align="center">folder_name</td>
<td align="center">str</td>
<td align="center">批量下载链接作品时，保存文件夹的名称</td>
<td align="center">Download</td>
</tr>
<tr>
<td align="center">name_format</td>
<td align="center">str</td>
<td align="center">文件保存时的命名规则，值之间使用空格分隔，支持：<code>id</code>：作品 ID；<code>desc</code>：作品描述；<code>create_time</code>：发布时间；<code>nickname</code>：账号昵称；<code>mark</code>：账号标识；<code>uid</code>：账号 ID；<code>type</code>：作品类型</td>
<td align="center">发布时间-作品类型-账号昵称-描述</td>
</tr>
<tr>
<td align="center">date_format</td>
<td align="center">str</td>
<td align="center">日期时间格式；<a href="https://docs.python.org/zh-cn/3/library/time.html?highlight=strftime#time.strftime">点击查看设置规则</a></td>
<td align="center">年-月-日 时:分:秒</td>
</tr>
<tr>
<td align="center">split</td>
<td align="center">str</td>
<td align="center">文件命名的分隔符</td>
<td align="center">-</td>
</tr>
<tr>
<td align="center">folder_mode</td>
<td align="center">bool</td>
<td align="center">是否将每个作品的文件储存至单独的文件夹，文件夹名称格式与 <code>name_format</code> 参数一致</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">music</td>
<td align="center">bool</td>
<td align="center">是否下载作品音乐</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">truncate</td>
<td align="center">int</td>
<td align="center">文件下载进度条中描述字符串的最大长度，该参数用于调整显示效果</td>
<td align="center">64</td>
</tr>
<tr>
<td align="center">storage_format</td>
<td align="center">str</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>采集数据持久化储存格式，支持：<code>csv</code>、<code>xlsx</code>、<code>sql</code>(SQLite)</td>
<td align="center">不保存</td>
</tr>
<tr>
<td align="center">cookie</td>
<td align="center">dict | str</td>
<td align="center"><a href="#supplement"><sup>4</sup></a>抖音网页版 Cookie, 必需参数; 建议通过程序写入配置文件，亦可手动编辑</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">cookie_tiktok</td>
<td align="center">dict | str</td>
<td align="center"><a href="#supplement"><sup>4</sup></a>TikTok 网页版 Cookie, 必需参数; 建议通过程序写入配置文件，亦可手动编辑</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">dynamic_cover</td>
<td align="center">bool</td>
<td align="center">是否下载视频作品动态封面图</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">static_cover</td>
<td align="center">bool</td>
<td align="center">是否下载视频作品静态封面图</td>
<td align="center">false</td>
</tr>
<tr>
<td align="center">proxy</td>
<td align="center">str</td>
<td align="center">抖音请求代理地址</td>
<td align="center">不使用代理</td>
</tr>
<tr>
<td align="center">proxy_tiktok</td>
<td align="center">str</td>
<td align="center">TikTok 请求代理地址</td>
<td align="center">不使用代理</td>
</tr>
<tr>
<td align="center"><a href="#twc">twc_tiktok</a></td>
<td align="center">str</td>
<td align="center">TikTok Cookie 的 ttwid 值，一般情况下无需设置</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">download</td>
<td align="center">bool</td>
<td align="center">是否开启项目的下载功能，如果关闭，程序将不会下载任何文件</td>
<td align="center">true</td>
</tr>
<tr>
<td align="center">max_size</td>
<td align="center">int</td>
<td align="center">作品文件大小限制，单位字节，超出大小限制的作品文件将会跳过下载</td>
<td align="center">无限制</td>
</tr>
<tr>
<td align="center">chunk</td>
<td align="center">int</td>
<td align="center">每次从服务器接收的数据块大小，单位字节</td>
<td align="center">2097152(2 MB)</td>
</tr>
<tr>
<td align="center">timeout</td>
<td align="center">int</td>
<td align="center">请求数据的超时限制，单位秒</td>
<td align="center">10</td>
</tr>
<tr>
<td align="center">max_retry</td>
<td align="center">int</td>
<td align="center">发送请求获取数据发生异常时重试的最大次数，设置为 <code>0</code> 代表关闭重试</td>
<td align="center">10</td>
</tr>
<tr>
<td align="center">max_pages</td>
<td align="center">int</td>
<td align="center">批量下载账号喜欢作品、收藏作品或者采集作品评论数据时，请求数据的最大次数（不包括异常重试）</td>
<td align="center">不限制</td>
</tr>
<tr>
<td align="center">run_command</td>
<td align="center">str</td>
<td align="center">设置程序启动执行的默认命令，相当于模拟用户输入序号或内容（多个序号或内容之间使用空格分隔）</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">ffmpeg</td>
<td align="center">str</td>
<td align="center"><a href="#supplement"><sup>3</sup></a><code>ffmpeg.exe</code> 路径，下载直播时使用，如果系统环境存在 <code>ffmpeg</code> 或者不想使用 <code>ffmpeg</code>，无需设置该参数</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">live_qualities</td>
<td align="center">str</td>
<td align="center"><a href="#supplement"><sup>3</sup></a>下载直播时的默认清晰度，支持设置为清晰度或者序号；当设置了该参数时，获取直播推流地址将会直接下载指定清晰度的直播文件，不再提示输入清晰度；参数示例：<code>FULL_HD1</code>、<code>HD1</code>、<code>1</code>、<code>2</code> 等</td>
<td align="center">无</td>
</tr>
<tr>
<td align="center">douyin_platform</td>
<td align="center">bool</td>
<td align="center"><a href="#supplement"><sup>5</sup></a>是否启用抖音平台功能</td>
<td align="center">true</td>
</tr>
<tr>
<td align="center">tiktok_platform</td>
<td align="center">bool</td>
<td align="center"><a href="#supplement"><sup>5</sup></a>是否启用 TikTok 平台功能</td>
<td align="center">true</td>
</tr>
<tr>
<td align="center">browser_info</td>
<td align="center">dict</td>
<td align="center">抖音平台浏览器信息，一般情况下无需修改</td>
<td align="center">内置参数</td>
</tr>
<tr>
<td align="center">browser_info_tiktok</td>
<td align="center">dict</td>
<td align="center">TikTok 平台浏览器信息，一般情况下仅需修改 <code>device_id</code> 参数，获取方式查阅 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6%95%99%E7%A8%8B.md">Cookie 获取教程</a></td>
<td align="center">内置参数</td>
</tr>
</tbody>
</table>
<div id="supplement">
<p><strong>补充说明：</strong></p>
<ol>
<li><a href="#mark">详见标识参数说明</a></li>
<li>设置为 <code>favorite</code> 时，需要确保账号喜欢作品公开可见，或者配置对应账号的登录 Cookie</li>
<li>该参数仅在部分模式和功能中生效，如果不需要使用相应的模式和功能，无需设置该参数</li>
<li>必须设置平台的 Cookie 才能使用该平台的数据采集和文件下载功能</li>
<li>如果不需要使用该平台的任何功能，可以将该参数设置为 <code>false</code></li>
</ol>
</div>
<h2>配置示例</h2>

```json
{
  "accounts_urls": [
    {
      "mark": "账号A",
      "url": "https://www.douyin.com/user/aaa",
      "tab": "post",
      "earliest": "2024/3/1",
      "latest": "2024/7/1",
      "enable": true
    },
    {
      "mark": "账号B",
      "url": "https://v.douyin.com/bbb",
      "tab": "favorite",
      "earliest": 30,
      "latest": "",
      "enable": false
    }
  ],
  "accounts_urls_tiktok": "参数规则与 accounts_urls 一致",
  "mix_urls": [
    {
      "mark": "",
      "url": "https://v.douyin.com/ccc",
      "enable": true
    },
    {
      "mark": "合集B",
      "url": "https://www.douyin.com/video/123",
      "enable": false
    }
  ],
  "mix_urls_tiktok": "参数规则与 mix_urls 一致",
  "owner_url": {
    "mark": "已登录 Cookie 的账号标识，可以设置为空字符串",
    "url": "已登录 Cookie 的账号主页链接"
  },
  "owner_url_tiktok": "参数规则与 owner_url 一致",
  "root": "C:\\DouK-Downloader",
  "folder_name": "SOLO",
  "name_format": "create_time uid id",
  "date_format": "%Y-%m-%d",
  "split": " ",
  "folder_mode": false,
  "music": false,
  "truncate": 32,
  "storage_format": "xlsx",
  "cookie": {
    "key-1": "value-1",
    "key-2": "value-2",
    "key-3": "value-3"
  },
  "cookie_tiktok": "参数规则与 cookie 一致",
  "dynamic_cover": false,
  "static_cover": false,
  "proxy": "http://127.0.0.1:9999",
  "proxy_tiktok": "参数规则与 proxy 一致",
  "twc_tiktok": "",
  "download": true,
  "max_size": 104857600,
  "chunk": 10485760,
  "timeout": 5,
  "max_retry": 10,
  "max_pages": 2,
  "run_command": "6 2 1",
  "ffmpeg": "C:\\DouK-Downloader\\ffmpeg.exe",
  "live_qualities": "1",
  "douyin_platform": true,
  "tiktok_platform": true,
  "browser_info": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "browser_platform": "Win32",
    "browser_name": "Chrome",
    "browser_version": "126.0.0.0",
    "engine_name": "Blink",
    "engine_version": "126.0.0.0",
    "os_name": "Windows",
    "os_version": "10",
    "webid": ""
  },
  "browser_info_tiktok": {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "app_language": "zh-Hans",
    "browser_language": "zh-SG",
    "browser_name": "Mozilla",
    "browser_platform": "Win32",
    "browser_version": "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "language": "zh-Hans",
    "os": "windows",
    "priority_region": "CN",
    "region": "US",
    "tz_name": "Asia/Shanghai",
    "webcast_language": "zh-Hans",
    "device_id": "1234567890"
  }
}
```

<h2>参数详解</h2>
<h3>下载喜欢作品</h3>

```json
{
  "accounts_urls": [
    {
      "mark": "",
      "url": "https://www.douyin.com/user/aaa",
      "tab": "favorite",
      "earliest": "",
      "latest": "",
      "enable": true
    },
    {
      "mark": "",
      "url": "https://v.douyin.com/bbb",
      "tab": "post",
      "earliest": "",
      "latest": "",
      "enable": true
    },
    {
      "mark": "",
      "url": "https://www.douyin.com/user/ccc",
      "tab": "favorite",
      "earliest": "",
      "latest": "",
      "enable": false
    }
  ]
}
```

<p>将待下载的账号信息写入配置文件，每个账号对应一个对象/字典，<code>tab</code> 参数设置为 <code>favorite</code> 代表批量下载喜欢作品，支持多账号；<code>accounts_urls_tiktok</code>参数规则一致。</p>
<p>下载账号喜欢作品需要确保账号喜欢作品公开可见，或者配置对应账号的登录 Cookie！</p>
<p><b>下载账号喜欢作品需要使用已登录的 Cookie，否则可能无法获取正确的账号信息！</b></p>
<h3>发布日期限制</h3>

```json
{
  "accounts_urls": [
    {
      "mark": "账号A",
      "url": "https://v.douyin.com/aaa",
      "tab": "post",
      "earliest": "2023/12/1",
      "latest": "",
      "enable": true
    },
    {
      "mark": "",
      "url": "https://v.douyin.com/bbb",
      "tab": "post",
      "earliest": 30,
      "latest": "2024/12/1",
      "enable": true
    }
  ]
}
```

<p>如果已经采集某账号的全部发布作品，建议设置 <code>earliest</code> 和 <code>latest</code> 参数以减少后续采集请求次数，提高程序运行效率；<code>accounts_urls_tiktok</code>参数规则一致。</p>
<p>示例：将 <code>earliest</code> 参数设置为 <code>2023/12/1</code>，程序获取账号发布作品数据时，不会获取早于 <code>2023/12/1</code> 的作品数据。</p>
<p>示例：将 <code>earliest</code> 参数设置为 <code>30</code>，<code>latest</code> 参数设置为 <code>2024/12/1</code>，程序获取账号发布作品数据时，仅获取 2024 年 12 月 1 日当天及之前 30 天内发布的作品数据。</p>
<p>示例：将 <code>earliest</code> 参数设置为 <code>15</code>，<code>latest</code> 参数设置为 <code>5</code>，程序获取账号发布作品数据时，仅获取前 5 天 ~ 前 20 天之间发布的作品数据。</p>
<h3>文件储存路径</h3>

```json
{
  "root": "C:\\DouK-Downloader",
  "folder_name": "SOLO"
}
```

<p>程序会将账号作品和合集作品的文件 和 记录的数据储存至 <code>C:\DouK-Downloader</code> 文件夹内，链接作品的文件会储存至 <code>C:\DouK-Downloader\SOLO</code> 文件夹内。</p>
<h3>文件名称格式</h3>

```json
{
  "name_format": "create_time uid id",
  "split": " @ "
}
```

<p>作品文件名称格式为: <code>发布时间 @ 作者UID @ 作品ID</code></p>
<ul>
<li>如果作品没有描述，文件名称的描述内容将替换为作品 ID。</li>
<li>批量下载链接作品时，如果在 <code>name_format</code> 参数中设置了 <code>mark</code> 字段，程序会自动替换为 <code>nickname</code> 字段。</li>
</ul>
<h3>日期时间格式</h3>

```json
{
  "date_format": "%Y-%m-%d"
}
```

<p>发布时间格式为：XXXX年-XX月-XX日，详细设置规则可以 <a href="https://docs.python.org/zh-cn/3/library/time.html?highlight=strftime#time.strftime">查看文档</a></p>
<h3>数据储存格式</h3>

```json
{
  "storage_format": "xlsx"
}
```

<p>使用 <code>XLSX</code> 格式储存程序采集数据。</p>
<h3>文件大小限制</h3>

```json
{
  "max_size": 104857600
}
```

<p>作品文件大小限制为 104857600 字节(100 MB)，超过该大小的作品文件会自动跳过下载；直播文件不受限制。</p>
<h3>文件分块下载</h3>

```json
{
  "chunk": 10485760
}
```

<p>下载文件时每次从服务器接收 10485760 字节 (10 MB)的数据块。</p>
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

<p>下载账号喜欢作品、收藏作品以及采集作品评论数据时，仅获取前 <code>2</code> 页数据；用于解决下载账号喜欢作品、收藏作品需要获取全部数据的问题，以及作品评论数据数量过多的采集问题。</p>
<p>不影响下载账号发布作品，如需控制账号发布作品数据获取次数，请使用 <code>earliest</code> 和 <code>latest</code> 参数实现。</p>
<h3>默认执行命令</h3>

```json
{
  "run_command": "6 1 1 Q"
}
```

<p>上述命令表示运行程序自动依次执行 <code>终端交互模式</code> -> <code>批量下载账号作品(抖音)</code> -> <code>使用 accounts_urls 参数的账号链接(推荐)</code> -> <code>退出程序</code></p>
<p>该参数可以实现设置默认启动模式、运行功能后自动退出、自动读取浏览器 Cookie 等高级自动化功能！</p>
<ul>其他示例：
<li><code>6 2</code>：代表依次执行 <code>终端交互模式</code> -> <code>批量下载账号作品(抖音)</code></li>
<li><code>8</code>：代表执行<code>Web API 模式</code></li>
<li><code>2 7</code>：代表依次执行<code>从浏览器读取 Cookie (抖音)</code> -> <code>Edge</code></li>
</ul>
<h3>程序代理设置</h3>

```json
{
  "proxy": "http://127.0.0.1:9999"
}
```

<p>程序获取网络数据时使用 <code>http://127.0.0.1:9999</code> 作为代理；程序会自动验证代理是否可用，如果代理不可用，则 <code>proxy</code> 参数不生效。</p>
<p>如果您的电脑使用了代理工具且未修改默认端口，可以尝试以下设置：</p>
<ul>
<li>Clash: <code>http://127.0.0.1:7890</code></li>
<li>v2rayN: <code>http://127.0.0.1:10809</code></li>
</ul>
<h1>高级配置</h1>
<p>如果想要进一步修改程序功能，可以编辑 <code>src/custom</code> 文件夹内容（仅适用于通过源码运行项目），按照注释指引和实际需求进行自定义修改。</p>
<b>部分可自定义设置的功能：</b>
<ul>
<li>设置作品文件下载的最大线程数量</li>
<li>设置文件名称的作品描述长度限制</li>
<li>设置非法字符替换规则</li>
<li>开启服务器模式局域网访问功能</li>
<li>设置服务器模式主机及端口</li>
<li><del>设置平台参数更新间隔</del></li>
<li>设置彩色交互提示颜色</li>
<li>设置请求数据延时间隔</li>
<li>设置自定义作品筛选规则</li>
<li>设置分批获取数据策略</li>
<li>设置服务器模式参数验证</li>
</ul>
<h1>功能介绍</h1>
<h2>从剪贴板读取 Cookie</h2>
<p>参考 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/docs/Cookie%E8%8E%B7%E5%8F%96%E6%95%99%E7%A8%8B.md">Cookie 提取教程</a>，手动从浏览器复制所需 Cookie 内容至剪贴板，再按照程序提示操作；程序会自动读取剪贴板的内容并将有效的 Cookie 写入配置文件。</p>
<p>成功写入配置文件后，程序会提示当前 Cookie 登录状态！</p>
<h2>从浏览器读取 Cookie</h2>
<p>自动读取本地浏览器的 Cookie 数据，并提取所需 Cookie 写入配置文件。</p>
<p>成功写入配置文件后，程序会提示当前 Cookie 登录状态！</p>
<p>Windows 系统需要以管理员身份运行程序才能读取 Chromium、Chrome、Edge 浏览器 Cookie！</p>
<h2><del>扫码登录获取 Cookie</del></h2>
<p><del>程序自动获取抖音登录二维码，随后会在终端输出二维码，并使用系统默认图片浏览器打开二维码图片，使用者通过抖音 APP 扫码并登录账号，操作后关闭二维码图片窗口，程序会自动检查登录结果并将登录后的 Cookie 写入配置文件。</del></p>
<p><b>注意：</b>扫码登录可能会导致抖音账号被风控，该功能仅限学习研究，未来可能禁用或移除该功能！</p>
<h2>终端交互模式</h2>
<p>功能最全面的模式，支持全部功能。</p>
<h3>批量下载账号作品(抖音)</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts_urls</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接；此选项仅支持批量下载账号发布页作品，暂不支持参数设置。</li>
<li>输入文本文档路径，读取文件包含的账号链接；此选项仅支持批量下载账号发布页作品，暂不支持参数设置。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/user/账号ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>如果需要大批量采集账号作品，建议启用 <code>src/custom/function.py</code> 文件的 <code>suspend</code> 方法。</p>
<p><b>下载账号喜欢作品时需要使用已登录的 Cookie，否则程序可能无法正常获取账号消息！</b></p>
<p>如果当前账号昵称或账号标识不是有效的文件夹名称时，程序会自动替换为账号 ID。</p>
<p>每个账号的作品会下载至 <code>root</code> 参数路径下的账号文件夹，账号文件夹格式为 <code>UID123456789_mark_类型</code> 或者 <code>UID123456789_账号昵称_类型</code></p>
<h3>批量下载链接作品(抖音)</h3>
<ol>
<li>手动输入待采集的作品链接。</li>
<li>输入文本文档路径，读取文件包含的作品链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/discover?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/search/关键词?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/channel/分区ID?modal_id=作品ID</code></li>
</ul>
<p>作品会下载至 <code>root</code> 参数和 <code>folder_name</code> 参数拼接成的文件夹。</p>
<h3>获取直播推流地址(抖音)</h3>
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
<li>程序调用 <code>ffmpeg</code> 下载直播时，关闭 DouK-Downloader 不会影响直播下载。</li>
<li><del>程序调用内置下载器下载直播时，需要保持 DouK-Downloader 运行直到直播结束。</del></li>
<li>程序询问是否下载直播时，输入直播清晰度或者对应序号即可下载，例如：下载最高清晰度输入 <code>FULL_HD1</code> 或者 <code>1</code> 均可。</li>
<li><del>程序调用内置下载器下载的直播文件，视频时长会显示为直播总时长，实际视频内容从下载时间开始，靠后部分的片段无法播放。</del></li>
<li>直播视频会下载至 <code>root</code> 参数路径下的 <code>Live</code> 文件夹。</li>
<li>按下 <code>Ctrl + C</code> 终止程序或 <code>ffmpeg</code> 并不会导致已下载文件丢失或损坏，但无法继续下载。</li>
</ul>
<h3>采集作品评论数据(抖音)</h3>
<p><strong>评论回复采集功能暂不开放！</strong></p>
<ol>
<li>手动输入待采集的作品链接。</li>
<li>输入文本文档路径，读取文件包含的作品链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/discover?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/search/关键词?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/channel/分区ID?modal_id=作品ID</code></li>
</ul>
<p>支持采集<del>评论回复</del>、评论表情、评论图片；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<p>储存名称格式：<code>作品123456789_评论数据</code></p>
<h3>批量下载合集作品(抖音)</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>mix_urls</code> 参数中的合集链接或作品链接。</li>
<li>获取当前登录 Cookie 的收藏合集信息，并由使用者选择需要下载的合集；该选项暂不支持设置合集标识。</li>
<li>输入合集链接，或者属于合集的任意一个作品链接；该选项暂不支持设置合集标识。</li>
<li>输入文本文档路径，读取文件包含的作品链接或合集链接；该选项暂不支持设置合集标识。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/note/作品ID</code></li>
<li><code>https://www.douyin.com/video/作品ID</code></li>
<li><code>https://www.douyin.com/discover?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/search/关键词?modal_id=作品ID</code></li>
<li><code>https://www.douyin.com/collection/合集ID</code></li>
<li><code>https://www.douyin.com/channel/分区ID?modal_id=作品ID</code></li>
</ul>
<p>如果需要大批量采集合集作品，建议启用 <code>src/custom/function.py</code> 文件的 <code>suspend</code> 方法。</p>
<p>如果当前合集标题或合集标识不是有效的文件夹名称时，程序会自动替换为合集 ID。</p>
<p>每个合集的作品会下载至 <code>root</code> 参数路径下的合集文件夹，合集文件夹格式为 <code>MIX123456789_mark_合集作品</code> 或者 <code>MIX123456789_合集标题_合集作品</code></p>
<h3>采集账号详细数据(抖音)</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts_urls</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接。</li>
<li>输入文本文档路径，读取文件包含的账号链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://v.douyin.com/分享码/</code></li>
<li><code>https://www.douyin.com/user/账号ID</code></li>
<li><code>https://www.douyin.com/user/账号ID?modal_id=作品ID</code></li>
</ul>
<p>重复获取相同账号数据时会储存为新的数据行，不会覆盖原有数据；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<h3>采集搜索结果数据(抖音)</h3>
<h4>搜索条件规则</h4>
<ul>
<li>
<strong>综合搜索参数顺序：</strong><code>关键词</code>;<code>总页数</code>;<code>排序依据</code>;<code>发布时间</code>;<code>视频时长</code>;<code>搜索范围</code>;<code>内容格式</code>
</li>
<li>
<strong>视频搜索参数顺序：</strong><code>关键词</code>;<code>总页数</code>;<code>排序依据</code>;<code>发布时间</code>;<code>视频时长</code>;<code>搜索范围</code>
</li>
<li>
<strong>用户搜索参数顺序：</strong><code>关键词</code>;<code>总页数</code>;<code>粉丝数量</code>;<code>用户类型</code>
</li>
<li>
<strong>直播搜索参数顺序：</strong><code>关键词</code>;<code>总页数</code>
</li>
</ul>
<h4>参数含义</h4>
<ul>
<li>排序依据：<code>0</code>：综合排序；<code>1</code>：最多点赞；<code>2</code>：最新发布</li>
<li>发布时间：<code>0</code>：不限；<code>1</code>：一天内；<code>7</code>：一周内；<code>180</code>：半年内</li>
<li>视频时长：<code>0</code>：不限；<code>1</code>：一分钟以内；<code>2</code>：一到五分钟；<code>3</code>：五分钟以上</li>
<li>搜索范围：<code>0</code>：不限；<code>1</code>：最近看过；<code>2</code>：还未看过；<code>3</code>：关注的人</li>
<li>内容形式：<code>0</code>：不限；<code>1</code>：视频；<code>2</code>：图文</li>
<li>粉丝数量：<code>0</code>：不限；<code>1</code>：1000以下；<code>2</code>：1000-1W；<code>3</code>：1W-10W；<code>4</code>：10W-100W；<code>5</code>：100W以上</li>
<li>用户类型：<code>0</code>：不限；<code>1</code>：普通用户；<code>2</code>：企业认证；<code>3</code>：个人认证</li>
</ul>
<p><strong>参数之间使用两个空格分隔；除了搜索关键词以外的参数均只支持输入数值；未输入的参数均视为 <code>0</code></strong></p>
<p>程序采集的搜索结果数据会储存至文件；暂不支持直接下载搜索结果作品；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<h4>参数输入示例</h4>
<h5>综合搜索/视频搜索</h5>
<p><strong>输入：</strong><code>猫咪</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
<th align="center">排序依据</th>
<th align="center">发布时间</th>
<th align="center">视频时长</th>
<th align="center">搜索范围</th>
<th align="center">内容形式</th>
</tr>
<tr>
<td align="center">猫咪</td>
<td align="center">1</td>
<td align="center">不限</td>
<td align="center">不限</td>
<td align="center">不限</td>
<td align="center">不限</td>
<td align="center">不限</td>
</tr>
</table>
<hr>
<p><strong>输入：</strong><code>猫咪&nbsp;&nbsp;2&nbsp;&nbsp;2&nbsp;&nbsp;7&nbsp;&nbsp;0&nbsp;&nbsp;1</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
<th align="center">排序依据</th>
<th align="center">发布时间</th>
<th align="center">视频时长</th>
<th align="center">搜索范围</th>
<th align="center">内容形式</th>
</tr>
<tr>
<td align="center">猫咪</td>
<td align="center">2</td>
<td align="center">最新发布</td>
<td align="center">一周内</td>
<td align="center">不限</td>
<td align="center">最近看过</td>
<td align="center">不限</td>
</tr>
</table>
<hr>
<p><strong>输入：</strong><code>猫咪&nbsp;&nbsp;10&nbsp;&nbsp;0&nbsp;&nbsp;0&nbsp;&nbsp;0&nbsp;&nbsp;3</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
<th align="center">排序依据</th>
<th align="center">发布时间</th>
<th align="center">视频时长</th>
<th align="center">搜索范围</th>
<th align="center">内容形式</th>
</tr>
<tr>
<td align="center">猫咪</td>
<td align="center">10</td>
<td align="center">不限</td>
<td align="center">不限</td>
<td align="center">不限</td>
<td align="center">关注的人</td>
<td align="center">不限</td>
</tr>
</table>
<hr>
<p><strong>输入：</strong><code>猫咪&nbsp;白&nbsp;&nbsp;5&nbsp;&nbsp;0&nbsp;&nbsp;180</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
<th align="center">排序依据</th>
<th align="center">发布时间</th>
<th align="center">视频时长</th>
<th align="center">搜索范围</th>
<th align="center">内容形式</th>
</tr>
<tr>
<td align="center">猫咪 白</td>
<td align="center">5</td>
<td align="center">不限</td>
<td align="center">半年内</td>
<td align="center">不限</td>
<td align="center">不限</td>
<td align="center">不限</td>
</tr>
</table>
<h5>用户搜索</h5>
<p><strong>输入：</strong><code>小姐姐&nbsp;&nbsp;10&nbsp;&nbsp;0&nbsp;&nbsp;0</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
<th align="center">粉丝数量</th>
<th align="center">用户类型</th>
</tr>
<tr>
<td align="center">小姐姐</td>
<td align="center">10</td>
<td align="center">不限</td>
<td align="center">不限</td>
</tr>
</table>
<hr>
<p><strong>输入：</strong><code>小姐姐&nbsp;&nbsp;5&nbsp;&nbsp;4&nbsp;&nbsp;3</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
<th align="center">粉丝数量</th>
<th align="center">用户类型</th>
</tr>
<tr>
<td align="center">小姐姐</td>
<td align="center">5</td>
<td align="center">10W-100W</td>
<td align="center">个人认证</td>
</tr>
</table>
<h5>直播搜索</h5>
<p><strong>输入：</strong><code>跳舞&nbsp;&nbsp;10</code></p>
<table>
<tr>
<th align="center" rowspan="2">含义</th>
<th align="center">关键词</th>
<th align="center">总页数</th>
</tr>
<tr>
<td align="center">跳舞</td>
<td align="center">10</td>
</tr>
</table>
<h3>采集抖音热榜数据(抖音)</h3>
<p>无需输入任何内容；采集 <code>抖音热榜</code>、<code>娱乐榜</code>、<code>社会榜</code>、<code>挑战榜</code> 数据并储存至文件；必须设置 <code>storage_format</code> 参数才能正常使用。</p>
<p>储存名称格式：<code>热榜数据_采集时间_热榜名称</code></p>
<h3>批量下载话题作品(抖音)</h3>
<p>暂不支持！</p>
<h3>批量下载收藏作品(抖音)</h3>
<p>无需输入任何内容；需要在配置文件写入已登录的 Cookie，并在 <code>owner_url</code> 参数填入对应的账号主页链接和账号标识（可选参数）；目前仅支持采集当前 Cookie 对应账号的收藏作品。</p>
<p>文件夹格式为 <code>UID123456789_mark_收藏作品</code> 或者 <code>UID123456789_账号昵称_收藏作品</code></p>
<h3>批量下载收藏夹作品(抖音)</h3>
<p>无需输入任何内容；需要在配置文件写入已登录的 Cookie，程序会自动获取当前 Cookie 账号的收藏夹数据并展示，根据程序提示输入收藏夹序号下载对应收藏夹作品文件，输入 <code>ALL</code> 下载全部收藏夹作品。</p>
<p>文件夹格式为 <code>CID123456789_收藏夹名称_收藏作品</code></p>
<h3>批量下载账号作品(TikTok)</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>accounts_urls_tiktok</code> 参数中的账号链接。</li>
<li>手动输入待采集的账号链接；此选项仅支持批量下载账号发布页作品，暂不支持参数设置。</li>
<li>输入文本文档路径，读取文件包含的账号链接；此选项仅支持批量下载账号发布页作品，暂不支持参数设置。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://www.tiktok.com/@TikTok号</code></li>
<li><code>https://www.tiktok.com/@TikTok号/video/作品ID</code></li>
</ul>
<p>如果需要大批量采集账号作品，建议启用 <code>src/custom/function.py</code> 文件的 <code>suspend</code> 方法。</p>
<p>如果当前账号昵称或账号标识不是有效的文件夹名称时，程序会自动替换为账号 ID。</p>
<p>每个账号的作品会下载至 <code>root</code> 参数路径下的账号文件夹，账号文件夹格式为 <code>UID123456789_mark_类型</code> 或者 <code>UID123456789_账号昵称_类型</code></p>
<h3>批量下载链接作品(TikTok)</h3>
<ol>
<li>手动输入待采集的作品链接。</li>
<li>输入文本文档路径，读取文件包含的作品链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://vm.tiktok.com/分享码/</code></li>
<li><code>https://www.tiktok.com/@TikTok号/video/作品ID</code></li>
</ul>
<p>作品会下载至 <code>root</code> 参数和 <code>folder_name</code> 参数拼接成的文件夹。</p>
<h3>批量下载合集作品(TikTok)</h3>
<ol>
<li>使用 <code>settings.json</code> 的 <code>mix_urls_tiktok</code> 参数中的合集链接或作品链接。</li>
<li>输入合集链接，或者属于合集的任意一个作品链接；该选项暂不支持设置合集标识。</li>
<li>输入文本文档路径，读取文件包含的作品链接或合集链接；该选项暂不支持设置合集标识。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://vt.tiktok.com/分享码/</code></li>
<li><code>https://www.tiktok.com/@TikTok号/playlist/合辑信息</code></li>
<li><code>https://www.tiktok.com/@TikTok号/collection/合辑信息</code></li>
</ul>
<p>如果需要大批量采集合集作品，建议启用 <code>src/custom/function.py</code> 文件的 <code>suspend</code> 方法。</p>
<p>如果当前合集标题或合集标识不是有效的文件夹名称时，程序会自动替换为合集 ID。</p>
<p>每个合集的作品会下载至 <code>root</code> 参数路径下的合集文件夹，合集文件夹格式为 <code>MIX123456789_mark_合集作品</code> 或者 <code>MIX123456789_合集标题_合集作品</code></p>
<h3>获取直播推流地址(TikTok)</h3>
<p>输入直播链接，不支持已结束的直播。</p>
<p>支持链接格式：</p>
<ul>
<li><code>https://vt.tiktok.com/分享码/</code></li>
<li><code>https://www.tiktok.com/@TikTok号/live</code></li>
</ul>
<p>下载说明：</p>
<ul>
<li>程序会询问用户是否下载直播视频，支持同时下载多个直播视频。</li>
<li>程序调用 <code>ffmpeg</code> 下载直播时，关闭 DouK-Downloader 不会影响直播下载。</li>
<li><del>程序调用内置下载器下载直播时，需要保持 DouK-Downloader 运行直到直播结束。</del></li>
<li>程序询问是否下载直播时，输入直播清晰度或者对应序号即可下载，例如：下载最高清晰度输入 <code>FULL_HD1</code> 或者 <code>1</code> 均可。</li>
<li><del>程序调用内置下载器下载的直播文件，视频时长会显示为直播总时长，实际视频内容从下载时间开始，靠后部分的片段无法播放。</del></li>
<li>直播视频会下载至 <code>root</code> 参数路径下的 <code>Live</code> 文件夹。</li>
<li>按下 <code>Ctrl + C</code> 终止程序或 <code>ffmpeg</code> 并不会导致已下载文件丢失或损坏，但无法继续下载。</li>
</ul>
<h3>批量下载视频原画(TikTok)</h3>
<p><strong>注意：本功能为实验性功能，依赖第三方 API 服务，可能不稳定或存在限制！</strong></p>
<ol>
<li>手动输入待采集的作品链接。</li>
<li>输入文本文档路径，读取文件包含的作品链接。</li>
</ol>
<p>支持链接格式：</p>
<ul>
<li><code>https://vm.tiktok.com/分享码/</code></li>
<li><code>https://www.tiktok.com/@TikTok号/video/作品ID</code></li>
</ul>
<p>作品会下载至 <code>root</code> 参数和 <code>folder_name</code> 参数拼接成的文件夹。</p>
<h2>后台监听模式</h2>
<h3>剪贴板监听下载</h3>
<p>程序会自动检测并提取剪贴板中的抖音和 TikTok 作品链接，并自动下载作品文件；如需关闭，请按下 Ctrl+C，或将剪贴板内容设置为“close”以停止监听！</p>
<h2>Web API 接口模式</h2>
<p>启动服务器，提供 API 调用功能；支持局域网远程访问，可以部署至私有服务器或者公开服务器，远程部署建议设置参数验证，防止恶意请求！</p>
<p>默认禁用局域网访问，如需开启，请修改 <code>src/custom/static.py</code> 文件的 <code>SERVER_HOST</code> 变量。</p>
<p><strong>启动该模式后，访问 <code>http://127.0.0.1:5555/docs</code> 或者 <code>http://127.0.0.1:5555/redoc</code> 可以查阅自动生成的文档！</strong></p>
<h3>API 调用示例代码</h3>
<pre>
from httpx import post
from rich import print


def demo():
headers = {"token": ""}
data = {
"detail_id": "0123456789",
"pages": 2,
}
api = "http://127.0.0.1:5555/douyin/comment"
response = post(api, json=data, headers=headers)
print(response.json())

demo()
</pre>
<h2>Web UI 交互模式</h2>
<p><b>项目代码已重构，该模式代码尚未更新，未来开发完成重新开放！</b></p>
<h2>启用/禁用作品下载记录</h2>
<ul>
<li>启用该功能：程序会记录下载成功的作品 ID，如果对作品文件进行移动、重命名或者删除操作，程序不会重复下载该作品，如果想要重新下载该作品，需要删除记录数据中对应的作品 ID。</li>
<li>禁用该功能：程序会在下载文件前检测文件是否存在，如果文件存在会自动跳过下载该作品，如果对作品文件进行移动、重命名或者删除操作，程序将会重新下载该作品。</li>
</ul>
<p>数据路径: <code>./Volume/DouK-Downloader.db</code> 的 <code>download_data</code> 数据表。</p>
<h2>删除指定下载记录</h2>
<p>输入作品 ID 或者作品完整链接（多个作品之间使用空格分隔，支持混合输入），删除作品下载记录中对应的数据，如果输入 <code>all</code>，代表清空作品下载记录数据！</p>
<h2>启用/禁用运行日志记录</h2>
<p>是否将程序运行日志记录保存到文件，默认关闭，日志文件保存路径：<code>./Volume/Log</code></p>
<p>如果在使用过程中发现程序 Bug，可以及时告知作者，并附上日志文件，日志记录有助于作者分析 Bug 原因和修复 Bug。</p>
<h2>检查程序版本更新</h2>
<p>程序会向 <code>https://github.com/JoeanAmier/TikTokDownloader/releases/latest</code>
发送请求获取最新 <code>Releases</code> 版本号，并提示是否存在新版本。</p>
<p>如果检查新版本失败，可能是访问 GitHub 超时，并非功能异常；如果存在新版本会提示新版本的 <code>URL</code> 地址，不会自动下载更新。</p>
<h1>其他功能说明</h1>
<h2>单次输入多个链接</h2>
<p><code>批量下载账号作品</code>、<code>批量下载链接作品</code>、<code>获取直播推流地址</code>、<code>采集作品评论数据</code>、<code>批量下载合集作品</code>、<code>采集账号详细数据</code>
功能支持单次输入多个链接，实现批量下载 / 提取功能；支持完整链接与分享链接混合输入；输入多个链接时，需要使用空格分隔；无需对复制的链接进行额外处理，程序会自动提取输入文本中的有效链接。</p>
<h2 id="mark">账号/合集标识说明</h2>
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
<p><strong>修改账号标识:</strong> 修改 <code>accounts_urls</code> 或 <code>accounts_urls_tiktok</code> 的 <code>mark</code> 参数，再次运行 <code>批量下载账号作品</code> 模式，程序会自动应用新的账号标识。</p>
<p><strong>修改合集标识:</strong> 修改 <code>mix_urls</code> 或 <code>mix_urls_tiktok</code> 的 <code>mark</code> 参数，再次运行 <code>批量下载合集作品</code> 模式，程序会自动应用新的账号标识。</p>
<h2>账号昵称/合集标题自动更新</h2>
<p>在 <code>批量下载账号作品</code> 和 <code>批量下载合集作品</code> 模式下，程序会自动判断账号昵称/合集标题是否发生变化，如果发生变化，程序会自动识别已下载作品文件名称中的账号昵称/合集标题，并修改至最新账号昵称/合集标题。</p>
<p>程序会优先使用账号标识/合集标识进行更新处理，如果账号标识/合集标识为空字符串，程序会自动使用账号昵称/合集标题进行更新处理。</p>
<h3>映射缓存数据</h3>
<p><strong>数据路径: <code>./Volume/DouK-Downloader.db</code> 的 <code>mapping_data</code> 数据表；</strong>
用于记录账号 / 合集标识和账号昵称，当账号 / 合集标识或账号昵称发生变化时，程序会对相应的文件夹和文件进行重命名更新处理。</p>
<p><strong>缓存数据仅供程序读取和修改，不建议手动编辑数据内容。</strong></p>

# 构建可执行文件指南

本指南将引导您通过 Fork 本仓库并执行 GitHub Actions 自动完成基于最新源码的程序构建和打包！

---

## 使用步骤

### 1. Fork 本仓库

1. 点击项目仓库右上角的 **Fork** 按钮，将本仓库 Fork 到您的个人 GitHub 账户中
2. 您的 Fork 仓库地址将类似于：`https://github.com/your-username/this-repo`

---

### 2. 启用 GitHub Actions

1. 前往您 Fork 的仓库页面
2. 点击顶部的 **Settings** 选项卡
3. 点击右侧的 **Actions** 选项卡
4. 点击 **General** 选项
5. 在 **Actions permissions** 下，选择 **Allow all actions and reusable workflows** 选项，点击 **Save** 按钮

---

### 3. 手动触发打包流程

1. 在您 Fork 的仓库中，点击顶部的 **Actions** 选项卡
2. 找到名为 **手动构建可执行文件** 的工作流
3. 点击右侧的 **Run workflow** 按钮：
    - 选择 **master** 或者 **develop** 分支
    - 点击 **Run workflow**

---

### 4. 查看打包进度

1. 在 **Actions** 页面中，您可以看到触发的工作流运行记录
2. 点击运行记录，查看详细的日志以了解打包进度和状态

---

### 5. 下载打包结果

1. 打包完成后，进入对应的运行记录页面
2. 在页面底部的 **Artifacts** 部分，您将看到打包的结果文件
3. 点击下载并保存到本地，即可获得打包好的程序

---

## 注意事项

1. **资源使用**：
    - Actions 的运行环境由 GitHub 免费提供，普通用户每月有一定的免费使用额度（2000 分钟）

2. **代码修改**：
    - 您可以自由修改 Fork 仓库中的代码以定制程序打包流程
    - 修改后重新触发打包流程，您将得到自定义的构建版本

3. **与主仓库保持同步**：
    - 如果主仓库更新了代码或工作流，建议您定期同步 Fork 仓库以获取最新功能和修复

---

## Actions 常见问题

### Q1: 为什么我无法触发工作流？

A: 请确认您已按照步骤 **启用 Actions**，否则 GitHub 会禁止运行工作流

### Q2: 打包流程失败怎么办？

A:

- 检查运行日志，了解失败原因
- 确保代码没有语法错误或依赖问题
- 如果问题仍未解决，可以在本仓库的 [Issues 页面](https://github.com/JoeanAmier/TikTokDownloader/issues) 提出问题

### Q3: 我可以直接使用主仓库的 Actions 吗？

A: 由于权限限制，您无法直接触发主仓库的 Actions。请通过 Fork 仓库的方式执行打包流程

<h1>常见问题与解决方案</h1>
<h2>响应内容不是有效的 JSON 数据</h2>
<p>可能是 Cookie 无效或者接口失效；请尝试清除 DNS 缓存，更新 Cookie，如果仍然无法解决，可能是接口失效，请考虑向作者反馈！</p>
<h2 id="twc">获取 ttwid 参数失败</h2>
<p>TikTok 平台的 Cookie ttwid 值无效；可能是当前账号被风控，请考虑更换账号，或者尝试设置 <code>twc_tiktok</code> 参数。</p>
<p><code>twc_tiktok</code> 参数设置教程：</p>
<ul>
<li>以无痕模式打开浏览器</li>
<li>按 <code>F12</code> 打开开发人员工具</li>
<li>选择 <code>网络</code> 选项卡</li>
<li>访问 <code>https://www.tiktok.com/</code></li>
<li>在 <code>筛选器</code> 输入框输入 <code>ttwid</code></li>
<li>在开发人员工具窗口选择任意一个数据包(如果无数据包，刷新网页)</li>
<li>检查 <code>响应标头</code> -> <code>Set-Cookie</code></li>
<li>复制 <code>ttwid=XXX</code> 内容</li>
<li>粘贴至配置文件的 <code>twc_tiktok</code> 参数</li>
</ul>
<p><code>Set-Cookie</code> 的内容格式为：<code>ttwid=XXX; Path=/; Domain=tiktok.com; Max-Age=31536000; HttpOnly; Secure; SameSite=None</code>，复制时只需要复制 <code>ttwid=XXX</code> 部分，而不是复制全部内容！</p>
<h2>采集数据而不下载文件</h2>
<p>将配置文件的 <code>download</code> 参数设置为 <code>false</code>，并设置 <code>storage_format</code> 参数，程序将不会下载任何文件，仅采集数据。</p>
<h2>请求超时：timed out</h2>
<p>网络异常；如果您的网络需要使用代理才能访问 TikTok，请在配置文件设置 <code>proxy</code> 参数！</p>
<h2>self 获取账号信息失败</h2>
<p>请把配置文件的 <code>owner_url</code> 参数修改为实际的抖音主页链接，获取方式请查阅 <a href="https://github.com/JoeanAmier/TikTokDownloader/issues/416">issue</a></p>
<h1>免责声明</h1>
<ol>
<li>使用者对本项目的使用由使用者自行决定，并自行承担风险。作者对使用者使用本项目所产生的任何损失、责任、或风险概不负责。</li>
<li>本项目的作者提供的代码和功能是基于现有知识和技术的开发成果。作者按现有技术水平努力确保代码的正确性和安全性，但不保证代码完全没有错误或缺陷。</li>
<li>本项目依赖的所有第三方库、插件或服务各自遵循其原始开源或商业许可，使用者需自行查阅并遵守相应协议，作者不对第三方组件的稳定性、安全性及合规性承担任何责任。</li>
<li>使用者在使用本项目时必须严格遵守 <a href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/LICENSE">GNU
    General Public License v3.0</a> 的要求，并在适当的地方注明使用了 <a
        href="https://github.com/JoeanAmier/TikTokDownloader/blob/master/LICENSE">GNU General Public License
    v3.0</a> 的代码。
</li>
<li>使用者在使用本项目的代码和功能时，必须自行研究相关法律法规，并确保其使用行为合法合规。任何因违反法律法规而导致的法律责任和风险，均由使用者自行承担。</li>
<li>使用者不得使用本工具从事任何侵犯知识产权的行为，包括但不限于未经授权下载、传播受版权保护的内容，开发者不参与、不支持、不认可任何非法内容的获取或分发。</li>
<li>本项目不对使用者涉及的数据收集、存储、传输等处理活动的合规性承担责任。使用者应自行遵守相关法律法规，确保处理行为合法正当；因违规操作导致的法律责任由使用者自行承担。</li>
<li>使用者在任何情况下均不得将本项目的作者、贡献者或其他相关方与使用者的使用行为联系起来，或要求其对使用者使用本项目所产生的任何损失或损害负责。</li>
<li>本项目的作者不会提供 DouK-Downloader 项目的付费版本，也不会提供与 DouK-Downloader 项目相关的任何商业服务。</li>
<li>基于本项目进行的任何二次开发、修改或编译的程序与原创作者无关，原创作者不承担与二次开发行为或其结果相关的任何责任，使用者应自行对因二次开发可能带来的各种情况负全部责任。</li>
<li>本项目不授予使用者任何专利许可；若使用本项目导致专利纠纷或侵权，使用者自行承担全部风险和责任。未经作者或权利人书面授权，不得使用本项目进行任何商业宣传、推广或再授权。</li>
<li>作者保留随时终止向任何违反本声明的使用者提供服务的权利，并可能要求其销毁已获取的代码及衍生作品。</li>
<li>作者保留在不另行通知的情况下更新本声明的权利，使用者持续使用即视为接受修订后的条款。</li>
</ol>
<b>在使用本项目的代码和功能之前，请您认真考虑并接受以上免责声明。如果您对上述声明有任何疑问或不同意，请不要使用本项目的代码和功能。如果您使用了本项目的代码和功能，则视为您已完全理解并接受上述免责声明，并自愿承担使用本项目的一切风险和后果。</b>
