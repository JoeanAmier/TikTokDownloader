# -*- coding: utf-8 -*-
"""
抖音下载器 —— DouK-Downloader 的极简桌面外壳 (类似 downkyi)
只保留两件事:
  1) 粘博主主页链接  -> 下载该博主全部作品
  2) 粘单个视频链接  -> 下载该视频
下载/签名/翻页/Cookie 全部复用 DouK 引擎 (src/),本文件只是个壳。
"""

import sys
import os
import re
import queue
import asyncio
import threading
import traceback
from pathlib import Path

# 快速解析:规范链接里直接抠 sec_uid / 作品ID,免去抓取整页(慢且易被限流)
USER_RE = re.compile(r"douyin\.com/user/([A-Za-z0-9_-]+)")
VIDEO_RE = re.compile(r"(?:/video/|modal_id=)(\d{19})|\b(\d{19})\b")

# 日志计数:引擎打印"共获取到 N 个"标记批次总数,每个文件完成打印"...文件下载成功"
TOTAL_RE = re.compile(r"共获取到\s*(\d+)\s*个")
SUCCESS_MARK = "文件下载成功"

# ---- 仓库根目录加入 sys.path,保证 import src.* 可用 ----
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ---- 把 stdout/stderr 重定向到队列,引擎(rich)的输出就能进日志区 ----
# (pythonw.exe 下 sys.stdout 本来是 None,这里必须替换掉)
LOG_QUEUE: "queue.Queue[str]" = queue.Queue()


class _QueueWriter:
    encoding = "utf-8"
    errors = "replace"

    def __init__(self, q):
        self._q = q

    def write(self, s):
        if s:
            self._q.put(s)
        return len(s) if s else 0

    def flush(self):
        pass

    def isatty(self):
        return False


sys.stdout = _QueueWriter(LOG_QUEUE)
sys.stderr = _QueueWriter(LOG_QUEUE)

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# ---- 引擎(在 stdout 重定向之后再导入) ----
from src.application import TikTokDownloader
from src.application.main_terminal import TikTok
from src.interface.template import API


# ---- 抖音"我的关注"接口(引擎没有,这里自建;纯 Cookie) ----
class _SelfProfile(API):
    """profile/self: 用 Cookie 拿到自己的 sec_uid"""
    def __init__(self, params, cookie="", proxy=None):
        super().__init__(params, cookie, proxy)
        self.api = f"{self.domain}aweme/v1/web/user/profile/self/"
    def generate_params(self):
        return self.params | {"publish_video_strategy_type": "2"}


class _Following(API):
    """following/list: 拉自己的关注列表(max_time 游标分页)"""
    def __init__(self, params, cookie="", proxy=None, sec_user_id="", max_time=0):
        super().__init__(params, cookie, proxy)
        self.api = f"{self.domain}aweme/v1/web/user/following/list/"
        self.sec_user_id = sec_user_id
        self.max_time = max_time
    def generate_params(self):
        return self.params | {
            "sec_user_id": self.sec_user_id, "offset": "0", "min_time": "0",
            "max_time": str(self.max_time), "count": "20", "source_type": "1",
        }


# ============================ 引擎封装 ============================
class Engine:
    """在独立线程里跑一个常驻 asyncio loop,所有引擎调用都丢到这个 loop。"""

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        self.app: "TikTokDownloader | None" = None
        self.tk: "TikTok | None" = None

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def submit(self, coro):
        """把协程丢到引擎 loop,返回 concurrent.futures.Future。"""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    # ---------- 初始化 ----------
    async def bootstrap(self):
        app = TikTokDownloader()
        await app.__aenter__()
        # 跳过首次免责声明的交互确认
        await app.database.update_config_data("Disclaimer", 1)
        app.check_config()
        await app.check_settings(False)   # 读取 settings.json(含 cookie),构建 parameter
        self.app = app
        self._rebuild_tk()

    def _rebuild_tk(self):
        self.tk = TikTok(self.app.parameter, self.app.database, server_mode=True)

    # ---------- Cookie ----------
    def cookie_logged_in(self) -> bool:
        """settings.json 里的 cookie 是否是登录态(含 sessionid_ss)。"""
        try:
            ck = self.app.settings.read().get("cookie", "")
        except Exception:
            return False
        if isinstance(ck, dict):
            return bool(ck.get("sessionid_ss"))
        return "sessionid_ss" in (ck or "")

    async def set_cookie(self, cookie_str: str):
        # 复用引擎的 Cookie 写入(校验 + 解析 + 落盘 settings.json)
        ok = self.app.cookie.run(cookie_str, tiktok=False)
        if ok:
            await self.app.check_settings()   # 重建 parameter
            self._rebuild_tk()
        return ok

    # ---------- 下载:博主全部作品 ----------
    async def download_account(self, url: str):
        m = USER_RE.search(url)
        if m:
            secs = [m.group(1)]   # 规范主页链接:直接拿 sec_uid,免抓整页
        else:
            print("正在解析链接(短链需联网展开,请稍候)…")
            links = await self.tk.links.run(url, "user")
            if isinstance(links, str):
                links = [links]
            secs = [s for s in (links or []) if isinstance(s, str) and s]
        if not secs:
            print("× 未能从链接提取账号 sec_user_id,请确认是博主【主页】链接")
            return
        for index, sec in enumerate(secs, start=1):
            await self._download_one_account(sec, index)
        print("\n=== 博主作品下载流程结束 ===")

    async def _download_one_account(self, sec: str, index: int = 1):
        """整号下载/更新单个博主: 整夹归主类 + 登记到 authors.json"""
        clean = self.tk.parameter.CLEANER
        base_root = self.tk.downloader.root
        print(f"\n>>> 第 {index} 个账号:拉取作品列表 …")
        raw = await self.tk.deal_account_detail(
            index, sec_user_id=sec, tab="post", source=True)   # source=True 拿原始数据(含分类)
        if not raw:
            print("× 没拉到作品(Cookie 失效? 链接不对?)")
            return
        # 整号:整个博主归到"主类"(出现最多的抖音分类),不拆散
        votes = {}
        for it in raw:
            c = clean.filter_name(self._category_of(it), "未分类") or "未分类"
            votes[c] = votes.get(c, 0) + 1
        cat = max(votes, key=votes.get)
        a0 = raw[0].get("author") or {}
        nick = a0.get("nickname") or sec
        uid = str(a0.get("uid") or "")
        print(f"共获取到 {len(raw)} 个作品,主类【{cat}】({nick}),下到 {cat}/UID_博主 …")
        self.register_author(sec, uid, nick, cat)
        cat_root = base_root.joinpath(cat)
        cat_root.mkdir(parents=True, exist_ok=True)
        self.tk.downloader.root = cat_root
        try:
            await self.tk._batch_process_detail(
                raw, api=False, mode="post", user_id=sec, mark="")
        finally:
            self.tk.downloader.root = base_root

    # ---------- 关注博主登记表(Volume/authors.json) ----------
    def _authors_path(self):
        from pathlib import Path
        return Path(self.tk.parameter.root).joinpath("authors.json")

    def load_authors(self) -> list:
        import json
        p = self._authors_path()
        try:
            data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        except Exception:
            data = {}
        return [{"sec": s, "uid": v.get("uid", ""), "nickname": v.get("nickname", ""),
                 "category": v.get("category", "未分类")} for s, v in data.items()]

    def register_author(self, sec, uid, nick, cat):
        import json
        p = self._authors_path()
        try:
            data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        except Exception:
            data = {}
        data[sec] = {"uid": uid, "nickname": nick, "category": cat}
        try:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as e:
            print("登记博主失败:", e)

    async def update_authors(self, secs: list):
        print(f">>> 更新 {len(secs)} 个关注博主 …")
        for i, sec in enumerate(secs, start=1):
            await self._download_one_account(sec, i)
        print("\n=== 关注博主更新结束 ===")

    async def _get_self_sec(self) -> str:
        try:
            sp = _SelfProfile(self.tk.parameter)
            r = await sp.request_data(sp.api, params=sp.generate_params(), data={},
                                      method="GET", encryption="GET", finished=True)
            return (r.get("user") or {}).get("sec_uid", "") if isinstance(r, dict) else ""
        except Exception as e:
            print("获取自己 sec_uid 失败:", e)
            return ""

    async def fetch_following(self):
        """拉我的抖音关注列表(纯 Cookie),合并进登记表(新关注先归'未分类')"""
        import json
        sec = await self._get_self_sec()
        if not sec:
            print("× 拿不到你的账号信息(Cookie 失效?)")
            return
        print(">>> 正在拉取你的关注列表 …")
        seen = {}
        mt = 0
        for _ in range(40):
            f = _Following(self.tk.parameter, sec_user_id=sec, max_time=mt)
            r = await f.request_data(f.api, params=f.generate_params(), data={},
                                     method="GET", encryption="GET", finished=True)
            if not isinstance(r, dict):
                break
            fl = r.get("followings") or []
            for x in fl:
                s = x.get("sec_uid")
                if s and s not in seen:
                    seen[s] = {"uid": str(x.get("uid", "")), "nickname": x.get("nickname", "")}
            if not r.get("has_more") or not fl or not r.get("min_time"):
                break
            mt = r["min_time"]
        p = self._authors_path()
        try:
            data = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        except Exception:
            data = {}
        added = 0
        for s, v in seen.items():
            if s not in data:
                data[s] = {"uid": v["uid"], "nickname": v["nickname"],
                           "category": "未分类", "following": True}
                added += 1
            else:
                data[s]["following"] = True
                if not data[s].get("nickname"):
                    data[s]["nickname"] = v["nickname"]
        try:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception as e:
            print("写登记表失败:", e)
        print(f"拉到 {len(seen)} 个关注博主,新增 {added} 个(未下载的归'未分类',下载/更新后自动归类)")

    # ---------- 下载:单个视频 ----------
    async def download_detail(self, url: str):
        root, params, logger = self.tk.record.run(self.tk.parameter)
        async with logger(root, console=self.tk.console, **params) as record:
            m = VIDEO_RE.search(url)
            if m:
                ids = [m.group(1) or m.group(2)]   # 规范视频链接/19位ID:直接用
            else:
                print("正在解析链接(短链需联网展开,请稍候)…")
                ids = await self.tk.links.run(url)
                ids = [i for i in (ids or []) if i]
            if not ids:
                print("× 未能从链接提取作品 ID,请确认是单个【视频】链接")
                return
            print(f">>> 共提取到 {len(ids)} 个作品,开始下载 ...")
            await self.tk._handle_detail(ids, False, record)
        print("\n=== 单个视频下载流程结束 ===")

    # ---------- 下载:我的收藏(默认收藏⭐,纯 Cookie,无需主页链接) ----------
    # 两级目录: Volume/{抖音分类}/UID{数字}_{博主}/视频  (分类取 video_tag 大类)
    @staticmethod
    def _category_of(item: dict) -> str:
        vt = item.get("video_tag") or []
        if isinstance(vt, list) and vt and isinstance(vt[0], dict):
            return vt[0].get("tag_name") or ""
        return ""

    async def download_collection(self):
        from src.interface import Collection
        print(">>> 正在拉取你的收藏列表(收藏多的话要等一会儿)…")
        collection = await Collection(self.tk.parameter).run()   # 纯 Cookie,自动翻全部页
        n = len(collection) if collection else 0
        if not n:
            print("× 没拉到收藏。Cookie 可能失效了 → 点「设置 Cookie」重贴一串再试")
            return
        clean = self.tk.parameter.CLEANER
        base_root = self.tk.downloader.root
        # 按 (分类, 博主) 两级分组
        groups = {}
        for it in collection:
            sec = (it.get("author") or {}).get("sec_uid") or ""
            cat = clean.filter_name(self._category_of(it), "未分类") or "未分类"
            groups.setdefault((cat, sec), []).append(it)
        cats = sorted({c for c, _ in groups})
        print(f"共获取到 {n} 个收藏作品,{len(cats)} 个分类,按 分类/博主 两级下载 …")
        try:
            for (cat, sec), items in groups.items():
                cat_root = base_root.joinpath(cat)
                cat_root.mkdir(parents=True, exist_ok=True)
                self.tk.downloader.root = cat_root   # 临时把下载根指到 分类 子目录
                if sec:
                    a = items[0].get("author") or {}
                    info = {"nickname": a.get("nickname", "未知作者"),
                            "sec_uid": sec, "uid": a.get("uid", "")}
                    uid = sec
                else:
                    info = {"nickname": "我的收藏", "sec_uid": "self", "uid": "self"}
                    uid = "self"
                await self.tk._batch_process_detail(
                    items, api=False, mode="collection",
                    info=info, user_id=uid, mark="",
                )
        finally:
            self.tk.downloader.root = base_root   # 复原下载根
        print("\n=== 我的收藏下载流程结束 ===")

    def download_root(self) -> str:
        try:
            return str(self.app.parameter.root)
        except Exception:
            return str(ROOT.joinpath("Volume"))


# ============================ 界面 ============================
class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = Engine()
        self.busy = False
        self._current_fut = None   # 当前下载任务的 future(给停止按钮用)
        self.dl_total = 0      # 当前批次作品总数(来自"共获取到 N 个")
        self.dl_done = 0       # 已完成文件计数
        self._linebuf = ""     # 日志按行处理用的缓冲
        self.author_vars = {}  # sec_uid -> BooleanVar(关注博主勾选)

        root.title("抖音下载器")
        root.geometry("820x740")
        root.minsize(680, 560)

        pad = {"padx": 10, "pady": 6}

        # 顶部:Cookie 状态 + 设置按钮
        top = ttk.Frame(root)
        top.pack(fill="x", **pad)
        self.cookie_var = tk.StringVar(value="Cookie:初始化中…")
        self.cookie_label = ttk.Label(top, textvariable=self.cookie_var, font=("Microsoft YaHei", 10, "bold"))
        self.cookie_label.pack(side="left")
        ttk.Button(top, text="设置 Cookie", command=self.on_set_cookie).pack(side="right")

        # 上部:关注的博主(按分类) —— 勾选后一键更新
        afr = ttk.LabelFrame(root, text="关注的博主（按分类，勾选后点更新拉新作品）")
        afr.pack(fill="x", **pad)
        abar = ttk.Frame(afr)
        abar.pack(fill="x", padx=8, pady=(6, 2))
        self.btn_fetch = ttk.Button(abar, text="⬇ 拉取关注列表", command=self.on_fetch_following)
        self.btn_fetch.pack(side="left")
        self.btn_update = ttk.Button(abar, text="🔄 更新选中", command=self.on_update_authors)
        self.btn_update.pack(side="left", padx=6)
        ttk.Button(abar, text="↻ 刷新", command=self.refresh_authors).pack(side="left")
        ttk.Button(abar, text="全选", command=lambda: self._set_all_authors(True)).pack(side="left")
        ttk.Button(abar, text="清空", command=lambda: self._set_all_authors(False)).pack(side="left", padx=6)
        acanvas = tk.Canvas(afr, height=150, highlightthickness=0)
        asb = ttk.Scrollbar(afr, orient="vertical", command=acanvas.yview)
        self.authors_inner = ttk.Frame(acanvas)
        self.authors_inner.bind(
            "<Configure>", lambda e: acanvas.configure(scrollregion=acanvas.bbox("all")))
        acanvas.create_window((0, 0), window=self.authors_inner, anchor="nw")
        acanvas.configure(yscrollcommand=asb.set)
        acanvas.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=(0, 8))
        asb.pack(side="right", fill="y", pady=(0, 8))
        # 鼠标滚轮(仅悬停在面板上时生效,不影响日志区滚动)
        acanvas.bind("<Enter>", lambda e: acanvas.bind_all(
            "<MouseWheel>", lambda ev: acanvas.yview_scroll(int(-ev.delta / 120), "units")))
        acanvas.bind("<Leave>", lambda e: acanvas.unbind_all("<MouseWheel>"))

        # 中部:URL 输入 + 两个下载按钮
        mid = ttk.LabelFrame(root, text="粘贴链接")
        mid.pack(fill="x", **pad)
        self.url_var = tk.StringVar()
        entry = ttk.Entry(mid, textvariable=self.url_var, font=("Consolas", 10))
        entry.pack(fill="x", padx=10, pady=(8, 4))
        entry.focus_set()

        btns = ttk.Frame(mid)
        btns.pack(fill="x", padx=10, pady=(0, 8))
        self.btn_account = ttk.Button(btns, text="⬇ 下载该博主全部作品", command=self.on_download_account)
        self.btn_account.pack(side="left")
        self.btn_detail = ttk.Button(btns, text="⬇ 下载单个视频", command=self.on_download_detail)
        self.btn_detail.pack(side="left", padx=8)
        self.btn_collection = ttk.Button(btns, text="⭐ 下载我的收藏", command=self.on_download_collection)
        self.btn_collection.pack(side="left")
        self.btn_stop = ttk.Button(btns, text="⏹ 停止", command=self.on_stop, state="disabled")
        self.btn_stop.pack(side="right")
        ttk.Label(
            mid,
            text="博主主页:https://www.douyin.com/user/MS4w...   |   单个视频:作品页链接 或 分享短链",
            foreground="#888",
        ).pack(anchor="w", padx=10, pady=(0, 6))

        # 下部:日志区
        logf = ttk.LabelFrame(root, text="运行日志")
        logf.pack(fill="both", expand=True, **pad)
        self.log = scrolledtext.ScrolledText(logf, height=14, font=("Consolas", 9), state="disabled", wrap="word")
        self.log.pack(fill="both", expand=True, padx=6, pady=6)

        # 底部:下载目录 + 打开文件夹
        bottom = ttk.Frame(root)
        bottom.pack(fill="x", **pad)
        self.dir_var = tk.StringVar(value="下载目录:(初始化中)")
        ttk.Label(bottom, textvariable=self.dir_var, foreground="#666").pack(side="left")
        ttk.Button(bottom, text="打开下载文件夹", command=self.on_open_folder).pack(side="right")

        self._set_buttons(False)
        self.root.after(120, self._drain_log)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # 启动引擎
        self._log_line("正在初始化下载引擎,请稍候 …\n")
        fut = self.engine.submit(self.engine.bootstrap())
        fut.add_done_callback(self._after(self._on_bootstrapped))

    # ---------- 工具:把回调切回 UI 线程 ----------
    def _after(self, fn):
        def cb(fut):
            self.root.after(0, lambda: fn(fut))
        return cb

    def _on_bootstrapped(self, fut):
        err = fut.exception()
        if err:
            self._log_line(f"× 引擎初始化失败:{err}\n")
            self._log_line(traceback.format_exc() + "\n")
            messagebox.showerror("初始化失败", str(err))
            return
        self._set_buttons(True)
        self.dir_var.set(f"下载目录:{self.engine.download_root()}")
        self._refresh_cookie()
        self.refresh_authors()
        self._log_line("引擎就绪。粘贴链接,点对应按钮即可下载。\n")

    # ---------- 关注博主面板 ----------
    def refresh_authors(self):
        for w in self.authors_inner.winfo_children():
            w.destroy()
        self.author_vars = {}
        try:
            authors = self.engine.load_authors()
        except Exception:
            authors = []
        if not authors:
            ttk.Label(self.authors_inner, foreground="#888",
                      text="（还没有关注的博主。粘博主主页链接下载一个后,会自动出现在这里。）").pack(anchor="w")
            return
        by_cat = {}
        for a in authors:
            by_cat.setdefault(a["category"] or "未分类", []).append(a)
        for cat in sorted(by_cat):
            ttk.Label(self.authors_inner, text=f"【{cat}】",
                      font=("Microsoft YaHei", 9, "bold")).pack(anchor="w", pady=(4, 0))
            for a in sorted(by_cat[cat], key=lambda x: x["nickname"]):
                var = tk.BooleanVar()
                self.author_vars[a["sec"]] = var
                ttk.Checkbutton(self.authors_inner, text="  " + (a["nickname"] or a["sec"][:12]),
                                variable=var).pack(anchor="w", padx=14)

    def _set_all_authors(self, val: bool):
        for var in self.author_vars.values():
            var.set(val)

    def on_update_authors(self):
        if self.busy:
            return
        secs = [s for s, v in self.author_vars.items() if v.get()]
        if not secs:
            messagebox.showwarning("提示", "请先勾选要更新的博主")
            return
        self._start_task(self.engine.update_authors(secs), "update")

    def on_fetch_following(self):
        if self.busy:
            return
        self._start_task(self.engine.fetch_following(), "fetch")

    def _refresh_cookie(self):
        if self.engine.cookie_logged_in():
            self.cookie_var.set("Cookie:✅ 已登录")
            self.cookie_label.configure(foreground="#1a7f37")
        else:
            self.cookie_var.set("Cookie:⚠ 未登录 / 未设置  → 点右侧“设置 Cookie”")
            self.cookie_label.configure(foreground="#c1121f")

    # ---------- 日志 ----------
    def _drain_log(self):
        try:
            while True:
                self._linebuf += LOG_QUEUE.get_nowait()
        except queue.Empty:
            pass
        if "\n" in self._linebuf:
            *lines, self._linebuf = self._linebuf.split("\n")
            for line in lines:
                self._process_log_line(line)
        self.root.after(120, self._drain_log)

    def _process_log_line(self, line: str):
        raw = line.rstrip("\r")
        m = TOTAL_RE.search(raw)
        if m:
            # 新批次开始:记录总数,序号归零
            self.dl_total = int(m.group(1))
            self.dl_done = 0
            self._log_line(raw + "\n")
            return
        if SUCCESS_MARK in raw:
            # 每个视频下完:前面空一行,行首打 [第N/共M]
            self.dl_done += 1
            tag = f"[{self.dl_done}/{self.dl_total}]" if self.dl_total else f"[{self.dl_done}]"
            self._log_line(f"\n{tag} {raw}\n")
            return
        self._log_line(raw + "\n")

    def _log_line(self, text: str):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---------- 按钮状态 ----------
    def _set_buttons(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        self.btn_account.configure(state=state)
        self.btn_detail.configure(state=state)
        self.btn_collection.configure(state=state)
        self.btn_update.configure(state=state)
        self.btn_fetch.configure(state=state)
        # 停止按钮与下载按钮相反:下载中才可点
        self.btn_stop.configure(state="disabled" if enabled else "normal")

    def _start_task(self, coro, what: str):
        if self.busy:
            return
        url = self.url_var.get().strip()
        if what in ("account", "detail") and not url:
            messagebox.showwarning("提示", "请先粘贴链接")
            return
        self.busy = True
        self.dl_total = 0      # 新任务:序号/总数归零
        self.dl_done = 0
        self._set_buttons(False)
        fut = self.engine.submit(coro)
        self._current_fut = fut
        fut.add_done_callback(self._after(self._on_task_done))

    def _on_task_done(self, fut):
        self.busy = False
        self._current_fut = None
        self._set_buttons(True)
        self.refresh_authors()   # 下完可能新增了关注博主,刷新面板
        if fut.cancelled():
            self._log_line("\n⏹ 已停止下载（已下完的文件保留，下次可续传）\n")
            return
        err = fut.exception()
        if err:
            self._log_line(f"× 出错:{err}\n")
            self._log_line(traceback.format_exc() + "\n")

    def on_stop(self):
        fut = self._current_fut
        if fut and not fut.done():
            self._log_line("\n⏹ 正在停止…\n")
            fut.cancel()
        else:
            self._log_line("（当前没有进行中的下载）\n")

    # ---------- 按钮回调 ----------
    def on_download_account(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("提示", "请先粘贴博主主页链接")
            return
        self._start_task(self.engine.download_account(url), "account")

    def on_download_detail(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("提示", "请先粘贴视频链接")
            return
        self._start_task(self.engine.download_detail(url), "detail")

    def on_download_collection(self):
        # 下载我的收藏不需要链接,纯 Cookie
        self._start_task(self.engine.download_collection(), "collection")

    def on_set_cookie(self):
        CookieDialog(self.root, self._do_set_cookie)

    def _do_set_cookie(self, cookie_str: str):
        cookie_str = (cookie_str or "").strip()
        if not cookie_str:
            return
        self._log_line("正在写入 Cookie …\n")

        async def _run():
            ok = await self.engine.set_cookie(cookie_str)
            return ok

        fut = self.engine.submit(_run())

        def done(fut):
            err = fut.exception()
            if err:
                self._log_line(f"× 写入 Cookie 失败:{err}\n")
                return
            if fut.result():
                self._log_line("✅ Cookie 写入成功\n")
            else:
                self._log_line("× 内容不是有效 Cookie,未写入\n")
            self._refresh_cookie()

        fut.add_done_callback(self._after(done))

    def on_open_folder(self):
        path = self.engine.download_root()
        try:
            os.makedirs(path, exist_ok=True)
            os.startfile(path)  # noqa
        except Exception as e:
            messagebox.showerror("打开失败", str(e))

    def on_close(self):
        try:
            self.engine.submit(self.engine.app.__aexit__(None, None, None))
        except Exception:
            pass
        self.root.after(150, self.root.destroy)


class CookieDialog(tk.Toplevel):
    def __init__(self, parent, on_ok):
        super().__init__(parent)
        self.title("设置 Cookie")
        self.geometry("560x320")
        self.on_ok = on_ok
        ttk.Label(
            self,
            text="把抖音网页登录后的整段 Cookie 粘贴到下面,然后点“保存”。\n"
                 "(F12→Network→任意 www.douyin.com 请求→Request Headers 里 cookie: 后面那一大串)",
            foreground="#555",
        ).pack(anchor="w", padx=10, pady=8)
        self.text = scrolledtext.ScrolledText(self, height=10, font=("Consolas", 9), wrap="word")
        self.text.pack(fill="both", expand=True, padx=10, pady=4)
        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=10, pady=8)
        ttk.Button(bar, text="保存", command=self._ok).pack(side="right")
        ttk.Button(bar, text="取消", command=self.destroy).pack(side="right", padx=8)
        self.text.focus_set()
        self.transient(parent)
        self.grab_set()

    def _ok(self):
        val = self.text.get("1.0", "end").strip()
        self.destroy()
        self.on_ok(val)


def main():
    root = tk.Tk()
    try:
        # Windows 上让 ttk 主题好看一点
        ttk.Style().theme_use("vista")
    except Exception:
        pass
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
