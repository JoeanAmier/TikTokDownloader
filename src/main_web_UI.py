from datetime import date
from urllib.parse import urlencode

from flask import render_template
from flask import request
from flask import url_for

from src.CookieTool import Cookie
from src.main_complete import TikTok


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
            for i, j in enumerate(keys):
                if index:
                    old_data[j][0] = new_data.get(j, values[i])
                else:
                    old_data[j] = new_data.get(j, values[i])

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
             "log"),
            ("./",
             "Download",
             "create_time author desc",
             "%Y-%m-%d %H.%M.%S",
             "-",
             "",
             False))
        update_settings(
            settings,
            convert,
            ("music",
             "dynamic",
             "original",
             "proxies"), (False, False, False, ""),
            True)
        self.settings.update(settings)
        if convert.get("cookie", False):
            self.cookie.extract(convert["cookie"], 0)

    def get_data(self, data) -> dict:
        def get_video_url(item):
            params = {
                "video_id": item[4],
                "ratio": "1080p",
            }
            result = {
                "视频下载地址": f"{self.download.video_id_api}?{urlencode(params)}",
                "原声下载地址": item[5][1],
                "动态封面图地址": item[6],
                "静态封面图地址": item[7],
            }
            return {"text": "\n".join(
                [f"{i}: {j}" for i, j in result.items()]), "preview": item[7]}

        def get_image_url(item):
            return {"text": "\n".join([f"{i}: {j}" for i, j in (
                    {f"Image_{i + 1} 下载地址": j for i, j in enumerate(item[4])} | {
                "原声下载地址": item[5][1]}).items()]), "preview": item[4][0]}

        if len(data) == 8:
            return get_video_url(data)
        elif len(data) == 6:
            return get_image_url(data)
        raise ValueError

    def single_acquisition(self):
        save, root, params = self.record.run(
            self._data["root"], format_=self._data["save"])
        with save(root, **params) as data:
            self.download.data = data
            id_ = self.request.run_alone(self.solo_url[0])
            if not id_:
                self.logger.error(f"{self.solo_url[0]} 获取 aweme_id 失败")
                return {
                    "text": "获取作品ID失败",
                    "preview": "static/images/blank.png"}
            result = self.download.run_alone(id_, self.solo_url[1])
            if isinstance(result, list):
                return self.get_data(result[0])
            if isinstance(result, str):
                return {"text": f"作品 {id_} 下载成功", "preview": result}

    def live_acquisition(self):
        if not (data := self.request.get_live_data(self.live_url)):
            self.logger.warning("获取直播数据失败")
            return {
                "text": "获取直播数据失败",
                "preview": "static/images/blank.png"}
        if not (data := self.request.deal_live_data(data)):
            return {
                "text": "提取直播推流地址失败",
                "preview": "static/images/blank.png"}
        result = {"主播昵称": data[0], "直播名称": data[1]} | data[2]
        for i, j in result.items():
            self.logger.info(f"{i}: {j}", False)
        return {
            "text": "\n".join([f"{i}: {j}" for i, j in result.items()]),
            "preview": data[3]}

    def webui_run(self, app):

        @app.route("/", methods=["GET"])
        def index():
            def initialize():
                if not self.check_config():
                    return False
                self.initialize(filename=f"{str(date.today())}.log")
                self.set_parameters()
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
                    "text": "无效的作品链接",
                    "preview": "static/images/blank.png"}
            self.solo_url = (url, download)
            return self.single_acquisition()

        @app.route('/live/', methods=['POST'])
        def live():
            url = request.form.get("url", False)
            if not url:
                return {
                    "text": "无效的直播链接",
                    "preview": "static/images/blank.png"}
            self.live_url = url
            return self.live_acquisition()

        return app
