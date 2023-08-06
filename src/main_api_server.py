from flask import request

from src.FileManager import Cache
from src.main_web_UI import WebUI


class APIServer(WebUI):
    works_keys = {
        "Video": (
            "作品ID",
            "作品描述",
            "发布时间",
            "UID",
            "作者昵称",
            "账号标识",
            "下载链接",
            "原声信息",
            "静态封面图",
            "动态封面图"),
        "Image": (
            "作品ID",
            "作品描述",
            "发布时间",
            "UID",
            "作者昵称",
            "账号标识",
            "下载链接",
            "原声信息"),
    }

    def __init__(self, colour, blacklist, xb, user_agent, code, settings):
        super().__init__(colour, blacklist, xb, user_agent, code, settings)

    def update_parameters(self, parameters):
        parameters = {
            i: j for i,
            j in parameters.items() if i in self.settings_keys}
        settings = self.settings.read()
        for i, j in parameters.items():
            settings[i] = j
        self.settings.update(settings)
        if c := parameters.get("cookie"):
            self.cookie.extract(c, 0)
        self.configuration(filename=self.filename)

    def add_params(self, params):
        save, root, params_ = self.record.run(
            self._data["root"], format_=self._data["save"])
        params["save"] = save
        params["root"] = root
        params["params"] = params_

    def format_data(self, data: list, type_: str):
        result = []
        keys = self.works_keys[type_]
        for item in data:
            dict_ = {keys[i]: j for i, j in enumerate(item)}
            result.append(dict_)
        return result

    def run_server(self, app):
        @app.route('/init/', methods=['POST'])
        def init():
            self.update_parameters(request.json)
            return {"message": "success"}

        @app.route('/account/', methods=['POST'])
        def account():
            url = request.json.get('url')
            url = self.request.run_alone(url, solo=True, user=True)
            if not url:
                return {"message": "link error"}
            params = {
                "num": 0,
                "mark": request.json.get('mark', ""),
                "url": url[0],
                "mode": request.json.get('mode', "post"),
                "earliest": request.json.get('earliest', ""),
                "latest": request.json.get('latest', ""),
            }
            self.manager = Cache(
                self.logger,
                self._data["root"],
                type_="UID",
                mark=self.mark,
                name=self.nickname)
            self.add_params(params)
            self.download.download = False
            self.get_account_works(**params)
            return {
                "video": self.format_data(self.download.video_data, "Video"),
                "image": self.format_data(self.download.image_data, "Image"),
                "message": "success",
            }

        @app.route('/detail/', methods=['POST'])
        def detail():
            return {}

        return app
