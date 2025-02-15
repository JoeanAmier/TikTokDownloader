from flask import render_template
from flask import request

from .main_web_UI import WebUI

__all__ = ["Server"]


class Server(WebUI):
    def __init__(self, parameter):
        super().__init__(parameter)

    def run_server(self, app):
        @app.route("/", methods=["GET"])
        def index():
            return render_template("server.html", preview=self.preview)

        @app.route("/settings/", methods=["POST"])
        def settings():
            return self.update_settings(request.json)

        @app.route("/single/", methods=["POST"])
        def single():
            url = request.json.get("url")
            if not url:
                return self.error_works
            return self.deal_single_works(url, False) or self.error_works

        return app
