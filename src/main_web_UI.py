from datetime import date

from flask import render_template
from flask import request
from flask import url_for

from src.CookieTool import Cookie
from src.main_complete import TikTok

BLANK_PREVIEW = "static/images/blank.png"


class WebUI(TikTok):
    def __init__(self):
        super().__init__()
        self.cookie = Cookie()
        self.solo_url = None
        self.live_url = None

    def update_parameters(self, parameters):
        """更新前端返回的parameters"""

        def update_settings(
                old_data: dict,
                new_data: dict,
                keys: tuple,
                values: tuple | None,
                index=False):
            for x, y in enumerate(keys):
                if index:
                    old_data[y][0] = new_data.get(y, values[x])
                else:
                    old_data[y] = new_data.get(y, values[x])

        convert = {}
        for i, j in parameters.items():
            convert[i] = True if j == "on" else j
        settings = self.settings.read()
        update_settings(
            settings,
            convert,
            ("root",
             "folder",
             "name",
             "time",
             "split",
             "save",
             "log",
             "chunk"),
            ("./",
             "Download",
             "create_time author desc",
             "%Y-%m-%d %H.%M.%S",
             "-",
             "",
             False,
             512 * 1024))
        update_settings(
            settings,
            convert,
            ("music",
             "dynamic",
             "original",
             "proxies"), (False, False, False, ""),
            True)
        self.settings.update(settings)
        if convert.get("cookie"):
            self.cookie.extract(convert["cookie"], 0)

    @staticmethod
    def get_data(data) -> dict:
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
            "preview": BLANK_PREVIEW}

    def single_acquisition(self):
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
                    "preview": BLANK_PREVIEW}
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
                "preview": BLANK_PREVIEW}

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
                "preview": BLANK_PREVIEW}
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

    def webui_run(self, app):

        @app.route("/", methods=["GET"])
        def index():
            def initialize():
                if not self.check_config():
                    return False
                self.initialize(filename=f"{str(date.today())}.log")
                self.set_parameters()
                self.request.headers['referer'] = "https://live.douyin.com"
                return True

            if not initialize():  # 初始化程序
                return "读取程序配置文件发生错误，请检查配置文件！"
            return render_template('index.html', **self._data)

        @app.route('/save/', methods=['POST'])
        def save():
            """保存配置并重新加载首页"""
            self.update_parameters(request.form)
            return url_for("index")

        @app.route('/solo/', methods=['POST'])
        def solo():
            url = request.form.get("url", False)
            download = {
                "true": True,
                "false": False,
                None: False}[
                request.form.get("download")]
            if not url:
                return {
                    "text": "无效的作品链接！",
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": BLANK_PREVIEW}
            self.solo_url = (url, download)
            return self.single_acquisition()

        @app.route('/live/', methods=['POST'])
        def live():
            url = request.form.get("url", False)
            if not url:
                return {
                    "text": "无效的直播链接！",
                    "url": {},
                    "best": "",
                    "preview": BLANK_PREVIEW}
            self.live_url = url
            return self.live_acquisition()

        return app
