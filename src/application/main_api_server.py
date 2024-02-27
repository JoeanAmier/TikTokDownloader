from flask import redirect
from flask import request

from src.DataAcquirer import Comment
from src.DataAcquirer import Live
from .main_web_UI import WebUI

__all__ = ['APIServer']


class APIServer(WebUI):
    def __init__(self, parameter, key=None):
        super().__init__(parameter, key)

    def _generate_record_params(self, data: dict, merge=True, **kwargs):
        root, params, logger = self.record.run(self.parameter,
                                               blank=data["source"],
                                               **kwargs)
        if not merge:
            return root, params, logger
        data["root"] = root
        data["params"] = params
        data["logger"] = logger

    def run_server(self, app):
        @app.route("/", methods=["GET"])
        def index():
            return redirect(
                "https://github.com/JoeanAmier/TikTokDownloader/wiki/Documentation")

        @app.route('/settings/', methods=['POST'])
        def settings():
            return self.update_settings(request.json)

        @app.route('/account/', methods=['POST'])
        def account():
            sec_user_ids = self.links.user(u := request.json.get("url"))
            if not sec_user_ids:
                self.logger.warning(m := f"{u} 提取账号 sec_user_id 失败")
                return {"data": None, "message": m}
            params = {
                "num": 0,
                "sec_user_id": sec_user_ids[0],
                "tab": request.json.get("tab", "post"),
                "earliest": request.json.get("earliest", ""),
                "latest": request.json.get("latest", ""),
                "pages": request.json.get("pages"),
                "api": True,
                "source": request.json.get("source", False),
                "cookie": request.json.get("cookie"),
            }
            self._generate_record_params(params)
            return {
                "data": (d := self.deal_account_works(**params)),
                "message": "success" if d else "failure",
            }

        @app.route('/detail/', methods=['POST'])
        def detail():
            tiktok, ids = self.links.works(u := request.json.get("url"))
            if not ids:
                self.logger.warning(m := f"{u} 提取作品 ID 失败")
                return {"data": None, "message": m}
            data = {
                "tiktok": tiktok,
                "ids": ids,
                "api": True,
                "source": request.json.get("source", False),
                "cookie": request.json.get("cookie"),
            }
            root, params, logger = self._generate_record_params(
                data, merge=False)
            with logger(root, console=self.console, **params) as record:
                return {
                    "data": (d := self.input_links_acquisition(
                        record=record,
                        **data)),
                    "message": "success" if d else "failure",
                }

        @app.route('/live/', methods=['POST'])
        def live():
            params = self._generate_live_params(
                *self.links.live(u := request.json.get("url")))
            if not params:
                self.logger.warning(m := f"{u} 提取直播 ID 失败")
                return {"data": None, "message": m}
            live_data = [
                Live(
                    self.parameter,
                    **i,
                    cookie=request.json.get("cookie"),
                ).run() for i in params]
            if not any(live_data):
                self.logger.warning(m := "获取直播数据失败")
                return {"data": None, "message": m}
            return {
                "data": (d := (live_data if request.json.get(
                    "source",
                    False) else self.extractor.run(
                    live_data,
                    None,
                    "live"))),
                "message": "success" if d else "failure",
            }

        @app.route('/comment/', methods=['POST'])
        def comment():
            tiktok, ids = self.links.works(u := request.json.get("url"))
            if not ids:
                self.logger.warning(m := f"{u} 提取作品 ID 失败")
                return {"data": None, "message": m}
            elif tiktok:
                return {"data": None, "message": "目前项目暂不支持采集 TikTok 作品评论数据！"}
            id_ = ids[0]
            name = f"作品{id_}_评论数据"
            data = {"source": request.json.get("source", False)}
            root, params, logger = self._generate_record_params(
                data, merge=False, type_="comment")
            with logger(root, name=name, console=self.console, **params) as record:
                if result := Comment(
                        self.parameter,
                        id_,
                        pages=request.json.get("pages"),
                        cookie=request.json.get("cookie"),
                ).run(
                    self.extractor,
                    record,
                    **data):
                    self.logger.info(f"作品评论数据已储存至 {name}")
                else:
                    self.logger.warning("采集评论数据失败")
            return {
                "data": (d := result or None),
                "message": "success" if d else "failure",
            }

        @app.route('/mix/', methods=['POST'])
        def mix():
            mix_id, ids = self.links.mix(u := request.json.get("url"))
            if not ids:
                self.logger.warning(m := f"{u} 获取作品 ID 或合集 ID 失败")
                return {"data": None, "message": m}
            params = {
                "mix_id": mix_id,
                "id_": ids[0],
                "api": True,
                "source": request.json.get("source", False),
                "cookie": request.json.get("cookie"),
            }
            self._generate_record_params(params, type_="mix")
            return {
                "data": (d := self._deal_mix_works(**params)),
                "message": "success" if d else "failure",
            }

        @app.route("/user/", methods=["POST"])
        def user():
            sec_user_ids = self.links.user(u := request.json.get("url"))
            if not sec_user_ids:
                self.logger.warning(m := f"{u} 提取账号 sec_user_id 失败")
                return {"data": None, "message": m}
            params = {"source": request.json.get("source", False)}
            self._generate_record_params(params, type_="user")
            users = [
                self._get_user_data(
                    i,
                    cookie=request.json.get("cookie"),
                ) for i in sec_user_ids]
            return {
                "data": (d := self._deal_user_data(
                    **params,
                    data=[
                        i for i in users if i])),
                "message": "success" if d else "failure",
            }

        @app.route("/search/", methods=["POST"])
        def search():
            params = self._enter_search_criteria(text=" ".join((
                request.json.get("keyword"),
                request.json.get("type", "0"),
                request.json.get("pages", "1"),
                request.json.get("sort_type", "0"),
                request.json.get("publish_time", "0"),
            )))
            if not all(params):
                return {"data": None, "message": "搜索参数无效！"}
            return {
                "data": (d := self._deal_search_data(
                    *params,
                    source=request.json.get(
                        "source",
                        False),
                    cookie=request.json.get("cookie"),
                )),
                "message": "success" if d else "failure",
            }

        @app.route("/hot/", methods=["POST"])
        def hot():
            time_, data = self._deal_hot_data(
                source=request.json.get("source", False))
            return {
                "time": time_,
                "data": data,
                "message": "success" if any(data) else "failure",
            }

        @app.route("/download/", methods=["POST"])
        def download():
            return {"message": "developing"}

        return app
