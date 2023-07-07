from flask import render_template

from src.main_complete import TikTok


class Server(TikTok):
    def __init__(self):
        super().__init__()

    def server_run(self, app):
        @app.route("/", methods=["GET"])
        def index():
            return render_template('server.html', )

        return app
