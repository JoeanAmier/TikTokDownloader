from flask import render_template
from flask import request

from src.DataAcquirer import Acquirer
from src.DataDownloader import Downloader
from src.Recorder import BaseLogger
from src.Recorder import NoneLogger
from src.main_web_UI import WebUI


class Server(WebUI):
    def __init__(self, colour, blacklist, xb, user_agent, code, settings):
        super().__init__(colour, blacklist, xb, user_agent, code, settings)

    def initialize(
            self,
            root="./",
            folder="Log",
            name="%Y-%m-%d %H.%M.%S",
            filename=None, ):
        self.logger = BaseLogger(self.colour)
        self.request = Acquirer(self.logger, self.xb, self.colour)
        self.download = Downloader(
            self.logger,
            None,
            self.xb,
            self.colour,
            self.blacklist,
            False)
        self.request.initialization(self.user_agent, self.code)
        self.download.initialization(self.user_agent, self.code)

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
                    "preview": self.preview}
            if not (result := self.download.run_alone(id_[0], False)):
                return {
                    "text": "提取作品数据失败！",
                    "author": None,
                    "describe": None,
                    "download": False,
                    "music": False,
                    "origin": False,
                    "dynamic": False,
                    "preview": self.preview}
            return self.get_data(result[0])

    def run_server(self, app):
        @app.route("/", methods=["GET"])
        def index():
            return render_template('server.html')

        @app.route('/solo/', methods=['POST'])
        def solo():
            url = request.json.get("url")
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
            self.solo_url = url
            return self.single_acquisition()

        return app
