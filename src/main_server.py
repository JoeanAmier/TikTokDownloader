from flask import render_template
from flask import request

from src.DataAcquirer import UserData
from src.DataDownloader import Download
from src.Recorder import BaseLogger
from src.Recorder import NoneLogger
from src.main_web_UI import WebUI

BLANK_PREVIEW = "static/images/blank.png"


class Server(WebUI):
    def __init__(self, colour, blacklist):
        super().__init__(colour, blacklist)
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
        self.logger = BaseLogger(self.colour)
        self.request = UserData(self.logger, self.xb, self.colour)
        self.download = Download(
            self.logger,
            None,
            self.xb,
            self.colour,
            self.blacklist)
        self.request.initialization()
        self.download.initialization()

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
            id_ = self.request.run_alone(self.solo_url, solo=True)
            self.download.tiktok = self.request.tiktok
            if not id_:
                return {
                    "text": "获取作品数据失败！",
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": BLANK_PREVIEW}
            if not (result := self.download.run_alone(id_[0], False)):
                return {
                    "text": "提取作品数据失败！",
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": BLANK_PREVIEW}
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
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": BLANK_PREVIEW}
            self.solo_url = url
            return self.single_acquisition()

        return app
