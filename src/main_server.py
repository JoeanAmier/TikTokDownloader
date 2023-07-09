from flask import render_template
from flask import request

from src.DataAcquirer import UserData
from src.DataDownloader import Download
from src.Recorder import BaseLogger
from src.Recorder import NoneLogger
from src.main_web_UI import WebUI


class Server(WebUI):
    def __init__(self):
        super().__init__()
        self.configuration()

    def configuration(self):
        if not self.check_config():
            return False
        self.initialize()
        self.set_parameters()
        return True

    def initialize(
            self,
            root="./",
            folder="Log",
            name="%Y-%m-%d %H.%M.%S",
            filename=None, ):
        self.logger = BaseLogger()
        self.request = UserData(self.logger)
        self.download = Download(self.logger, None)

    def set_parameters(self):
        self.download.cookie = self._data["cookie"]
        self.request.cookie = self._data["cookie"]
        self.request.time = "%Y-%m-%d"
        self.download.time = "%Y-%m-%d"
        self.request.proxies = self._data["proxies"]
        self.download.proxies = self.request.proxies
        self.download.download = False
        self.request.retry = self._data["retry"]
        self.download.retry = self._data["retry"]

    def single_acquisition(self):
        with NoneLogger() as data:
            self.download.data = data
            id_ = self.request.run_alone(self.solo_url)
            self.download.tiktok = self.request.tiktok
            if not id_:
                return {
                    "text": "获取作品数据失败！",
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": "static/images/blank.png"}
            if not (result := self.download.run_alone(id_, False)):
                return {
                    "text": "提取作品数据失败！",
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": "static/images/blank.png"}
            return self.get_data(result[0])

    def server_run(self, app):
        @app.route("/", methods=["GET"])
        def index():
            return render_template('server.html')

        @app.route('/solo/', methods=['POST'])
        def solo():
            url = request.form.get("url", False)
            if not url:
                return {
                    "text": "无效的作品链接！",
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": "static/images/blank.png"}
            self.solo_url = url
            return self.single_acquisition()

        return app
