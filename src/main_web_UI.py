from flask import render_template

from src.main_complete import TikTok


class WebUI(TikTok):
    def __init__(self):
        super().__init__()

    def webui_run(self, app):

        @app.route("/")
        def index():
            def initialize():
                if not self.check_config():
                    return False
                self.initialize()
                self.set_parameters()
                return True

            if not initialize():  # 初始化程序
                return "读取程序配置文件发生错误，请检查配置文件！"

            return render_template('index.html')

        return app
