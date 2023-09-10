from datetime import date

from flask import render_template
from flask import request
from flask import url_for

from src.CookieTool import Cookie
from src.main_complete import TikTok


class WebUI(TikTok):
    settings_keys = (
        "root",
        "folder",
        "name",
        "time",
        "split",
        "music",
        "save",
        "cookie",
        "dynamic",
        "original",
        "proxies",
        "log",
        "retry",
        "max_size",
        "chunk",
        "pages",
    )

    def __init__(self, colour, blacklist, xb, user_agent, code, settings):
        super().__init__(colour, blacklist, xb, user_agent, code, settings)
        self.cookie = Cookie(self.settings, colour)
        self.preview = "static/images/blank.png"
        self.filename = f"{str(date.today())}.log"
        self.configuration(filename=self.filename)
        self.solo_url = None
        self.live_url = None

    @staticmethod
    def update_settings(
            old_data: dict,
            new_data: dict,
            keys: tuple,
            values: tuple | None,
            index=False):
        for x, y in enumerate(keys):
            if index:
                old_data[y][0] = new_data.get(y, values[x] if values else None)
            else:
                old_data[y] = new_data.get(y, values[x] if values else None)

    def update_parameters(self, parameters):
        """更新前端返回的 parameters"""
        parameters = {
            i: j for i,
            j in parameters.items() if i in self.settings_keys}
        convert = {i: j == "on" or j for i, j in parameters.items()}
        settings = self.settings.read()
        self.update_settings(
            settings,
            convert,
            ("root",
             "folder",
             "name",
             "time",
             "split",
             "save",
             "log",
             "chunk",
             "music",
             "dynamic",
             "original",
             "proxies",
             "max_size",),
            ("./",
             "Download",
             "create_time nickname desc",
             "%Y-%m-%d %H.%M.%S",
             "-",
             "",
             False,
             512 * 1024,
             False,
             False,
             False,
             "",
             0))
        self.settings.update(settings)
        if c := convert.get("cookie"):
            self.cookie.extract(c)
        self.configuration(filename=self.filename)

    def get_data(self, data) -> dict:
        def get_video_url(item):
            result = {
                "text": "提取作品下载地址成功！",
                "author": item[4],
                "describe": item[1],
                "download": item[6],
                "music": item[7][1],
                "origin": item[8],
                "dynamic": item[9],
                "preview": item[8]
            }
            return result

        def get_image_url(item):
            result = {
                "text": "提取作品下载地址成功！",
                "author": item[4],
                "describe": item[1],
                "download": item[6],
                "music": item[7][1],
                "origin": False,
                "dynamic": False,
                "preview": item[6][0],
            }
            return result

        if len(data) == 10:
            return get_video_url(data)
        elif len(data) == 8:
            return get_image_url(data)
        return {
            "text": "服务器发生异常！",
            "author": None,
            "describe": None,
            "download": False,
            "music": False,
            "origin": False,
            "dynamic": False,
            "preview": self.preview}

    def single_acquisition(self):
        self.request.headers['Referer'] = "https://www.douyin.com/"
        save, root, params = self.record.run(
            self._data["root"], format_=self._data["save"])
        with save(root, **params) as data:
            self.download.data = data
            id_ = self.request.run_alone(self.solo_url[0], solo=True)
            if not id_:
                self.logger.error(f"{self.solo_url[0]} 获取作品ID失败")
                return {
                    "text": "获取作品数据失败！",
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": self.preview}
            self.download.tiktok = self.request.tiktok
            result = self.download.run_alone(id_[0], self.solo_url[1])
            if isinstance(result, list):
                return self.get_data(result[0])
            if isinstance(result, str):
                return {"text": f"作品 {id_[0]} 下载成功！",
                        "author": "不显示",
                        "describe": "不显示",
                        "download": False,
                        "music": False,
                        "origin": False,
                        "dynamic": False,
                        "preview": result}
            return {
                "text": "获取作品数据失败！",
                "author": None,
                "describe": None,
                "download": False,
                "music": False,
                "origin": False,
                "dynamic": False,
                "preview": self.preview}

    def live_acquisition(self):
        if not (
                data := self.request.run_live(
                    self.live_url,
                    solo=True)):
            self.logger.warning("获取直播数据失败")
            return {
                "text": "获取直播数据失败！",
                "urls": {},
                "best": "",
                "preview": self.preview}
        data = data[0]
        for i, j in ({"主播昵称": data[0], "直播名称": data[1],
                      "在线观众": data[5], "观看次数": data[4]} | data[2]).items():
            self.logger.info(f"{i}: {j}", False)
        return {
            "text": f"主播昵称: {data[0]}\n直播标题: {data[1]}\n在线观众: {data[5]} - 观看次数: {data[4]}",
            "urls": data[2],
            "best": min(
                data[2].values(),
                key=lambda x: x[0]),
            "preview": data[3]}

    def run_server(self, app):

        @app.route("/", methods=["GET"])
        def index():
            return render_template('index.html', **self._data)

        @app.route('/save/', methods=['POST'])
        def save():
            """保存配置并重新加载首页"""
            self.update_parameters(request.json)
            return url_for("index")

        @app.route('/solo/', methods=['POST'])
        def solo():
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
            return self.single_acquisition()

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
            return self.live_acquisition()

        return app
