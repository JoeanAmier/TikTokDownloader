from flask import request

from src.DataAcquirer import Comment
from src.DataAcquirer import Live
from src.main_web_UI import WebUI

__all__ = ['APIServer']


class APIServer(WebUI):
    def __init__(self, parameter):
        super().__init__(parameter)

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
                "api": True,
                "source": request.json.get("source", False),
            }
            self._generate_record_params(params)
            return {
                "data": self.deal_account_works(**params),
                "message": "success",
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
            }
            root, params, logger = self._generate_record_params(
                data, merge=False)
            with logger(root, **params) as record:
                return {
                    "data": self.input_links_acquisition(
                        record=record,
                        **data),
                    "message": "success",
                }

        @app.route('/live/', methods=['POST'])
        def live():
            params = self._generate_live_params(
                *self.links.live(u := request.json.get("url")))
            if not params:
                self.logger.warning(m := f"{u} 提取直播 ID 失败")
                return {"data": None, "message": m}
            live_data = [Live(self.parameter, **i).run() for i in params]
            if not [i for i in live_data if i]:
                self.logger.warning(m := "获取直播数据失败")
                return {"data": None, "message": m}
            return {
                "data": live_data if request.json.get(
                    "source",
                    False) else self.extractor.run(
                    live_data,
                    None,
                    "live"),
                "message": "success",
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
            with logger(root, name=name, **params) as record:
                if result := Comment(
                        self.parameter,
                        id_, pages=request.json.get("pages")).run(
                    self.extractor,
                    record,
                    **data):
                    self.logger.info(f"作品评论数据已储存至 {name}")
                else:
                    self.logger.warning("采集评论数据失败")
            return {
                "data": result or None,
                "message": "success",
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
            }
            self._generate_record_params(params, type_="mix")
            return {
                "data": self._deal_mix_works(**params),
                "message": "success",
            }

        @app.route("/user/", methods=["POST"])
        def user():
            sec_user_ids = self.links.user(u := request.json.get("url"))
            if not sec_user_ids:
                self.logger.warning(m := f"{u} 提取账号 sec_user_id 失败")
                return {"data": None, "message": m}
            params = {"source": request.json.get("source", False)}
            self._generate_record_params(params, type_="user")
            users = [self._get_user_data(i) for i in sec_user_ids]
            return {
                "data": self._deal_user_data(
                    **params,
                    data=[
                        i for i in users if i]),
                "message": "success",
            }

        @app.route("/search/", methods=["POST"])
        def search():
            params = self._enter_search_criteria(text=" ".join((
                request.json.get("keyword"),
                request.json.get("type", "0"),
                request.json.get("pages", "1"),
                request.json.get("sort", "0"),
                request.json.get("publish", "0"),
            )))
            if not all(params):
                return {"data": None, "message": "搜索参数无效！"}
            return {
                "data": self._deal_search_data(
                    *params,
                    source=request.json.get(
                        "source",
                        False)),
                "message": "success",
            }

        @app.route("/hot/", methods=["POST"])
        def hot():
            time_, data = self._deal_hot_data(
                source=request.json.get("source", False))
            return {
                "time": time_,
                "data": data,
                "message": "success",
            }

        return app
