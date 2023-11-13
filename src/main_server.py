from flask import render_template
from flask import request

from src.Customizer import verify_token
from src.main_web_UI import WebUI


class Server(WebUI):
    def __init__(self, parameter):
        super().__init__(parameter)

    def run_server(self, app):
        @app.route("/", methods=["GET"])
        def index():
            return render_template('server.html', preview=self.preview)

        @app.route('/settings/', methods=['POST'])
        def settings():
            """保存配置并重新加载首页"""
            return self.update_settings(request.json)

        @app.route('/single/', methods=['POST'])
        def single():
            url = request.json.get("url")
            if not url:
                return self.error_works
            if verify_token(request.json.get("token")):
                return self.deal_single_works(url, False) or self.error_works
            return self.error_works

        return app
