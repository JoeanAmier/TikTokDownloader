from flask import render_template
from flask import request
from flask import url_for

from src.main_complete import TikTok


class WebUI(TikTok):
    def __init__(self, parameter):
        super().__init__(parameter)
        self.cookie = parameter.cookie
        self.preview = parameter.preview

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
                     ("chunk", 512 * 1024),
                     ("max_retry", 10),
                     ("max_pages", 0),
                     ("default_mode", 0)):
            try:
                data[i] = int(data[i])
            except ValueError:
                data[i] = j

    def update_settings(self, data: dict):
        self._convert_bool(data)
        # print(data)  # 调试使用
        self.parameter.update_settings_data(data)

    def run_server(self, app):

        @app.route("/", methods=["GET"])
        def index():
            return render_template(
                'index.html',
                **self.parameter.get_settings_data(),
                preview=self.preview)

        @app.route('/update/', methods=['POST'])
        def update():
            """保存配置并重新加载首页"""
            self.update_settings(request.json)
            return url_for("index")

        @app.route('/single/', methods=['POST'])
        def single():
            url = request.json.get("url")
            download = request.json.get("download", False)
            if not url:
                return {
                    "text": "无效的作品链接！",
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": self.preview}
            self.solo_url = (url, download)
            return self.works_interactive()

        @app.route('/live/', methods=['POST'])
        def live():
            url = request.json.get("url")
            if not url:
                return {
                    "text": "无效的直播链接！",
                    "url": {},
                    "best": "",
                    "preview": self.preview}
            self.live_url = url
            return self.live_interactive()

        return app
