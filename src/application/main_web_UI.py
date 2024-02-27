from flask import render_template
from flask import request
from flask import url_for

from src.DataAcquirer import Live
from .main_complete import TikTok

__all__ = ["WebUI"]


class WebUI(TikTok):
    def __init__(self, parameter, key=None):
        super().__init__(parameter, key)
        self.cookie = parameter.cookie
        self.preview = parameter.preview
        self.error_works = {
            "text": "获取作品数据失败！",
            "author": None,
            "describe": None,
            "download": False,
            "music": False,
            "origin": False,
            "dynamic": False,
            "preview": self.preview}
        self.error_live = {
            "text": "提取直播数据失败！",
            "flv": {},
            "m3u8": {},
            "best": "",
            "preview": self.preview}

    @staticmethod
    def _convert_bool(data: dict):
        for i in (
                "folder_mode",
                "music",
                "dynamic_cover",
                "original_cover",
                "download"):
            data[i] = {"on": True, None: False}[data.get(i)]
        for i, j in (("max_size", 0),
                     ("chunk", 1024 * 1024),
                     ("max_retry", 5),
                     ("max_pages", 0),):
            try:
                data[i] = int(data[i])
            except ValueError:
                data[i] = j

    def update_settings(self, data: dict, api=True):
        if not api:
            self._convert_bool(data)
        # print(data)  # 调试使用
        return self.parameter.update_settings_data(data)

    def deal_single_works(self, url: str, download: bool) -> dict:
        tiktok, ids = self.links.works(url)
        if not ids:
            self.logger.warning(f"{url} 提取作品 ID 失败")
            return {}
        root, params, logger = self.record.run(self.parameter)
        with logger(root, console=self.console, **params) as record:
            return self.generate_works_data(d) if (d := self.input_links_acquisition(
                tiktok, ids[:1], record, not download)) else {}

    def generate_works_data(self, data: list[dict] | str) -> dict:
        if isinstance(data, str):
            return self.error_works | {"text": "后台下载作品成功！", "preview": data}
        data = data[0]
        return {
            "text": "获取作品数据成功！",
            "author": data["nickname"],
            "describe": data["desc"],
            "download": data["downloads"] if data["type"] == "视频" else (
                d := data["downloads"].split()),
            "music": data["music_url"],
            "origin": data["origin_cover"],
            "dynamic": data["dynamic_cover"],
            "preview": data["origin_cover"] or d[0]}

    def deal_live_data(self, url: str) -> dict:
        params = self._generate_live_params(*self.links.live(url))
        if not params:
            return {}
        live_data = [Live(self.parameter, **params[0]).run(), ]
        live_data = self.extractor.run(live_data, None, "live")[0]
        if not all(live_data):
            return {}
        if live_data["status"] == 4:
            return self.error_live | {"text": "当前直播已结束！"}
        return self.generate_live_data(live_data)

    @staticmethod
    def generate_live_data(data: dict) -> dict:
        return {
            "text": "\n".join((f"直播标题: {data["title"]}",
                               f"主播昵称: {data["nickname"]}",
                               f"在线观众: {data["user_count_str"]}",
                               f"观看次数: {data["total_user_str"]}",)),
            "flv": data["flv_pull_url"],
            "m3u8": data["hls_pull_url_map"],
            "best": list(data["flv_pull_url"].values())[0],
            "preview": data["cover"]}

    def run_server(self, app):

        @app.route("/", methods=["GET"])
        def index():
            return render_template(
                'index.html',
                **self.parameter.get_settings_data(),
                preview=self.preview)

        @app.route('/settings/', methods=['POST'])
        def settings():
            """保存配置并重新加载首页"""
            self.update_settings(request.json, False)
            return url_for("index")

        @app.route('/single/', methods=['POST'])
        def single():
            url = request.json.get("url")
            download = request.json.get("download", False)
            if not url:
                return self.error_works
            return self.deal_single_works(url, download) or self.error_works

        @app.route('/live/', methods=['POST'])
        def live():
            url = request.json.get("url")
            if not url:
                return self.error_live
            return self.deal_live_data(url) or self.error_live

        return app
