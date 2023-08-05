from flask import request

from src.main_web_UI import WebUI


class APIServer(WebUI):

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

    def run_server(self, app):
        @app.route('/init/', methods=['POST'])
        def init():
            print(request.json)
            self.update_parameters(request.json)
            return {"message": "success"}

        @app.route('/user/', methods=['POST'])
        def user():
            print(request.form)

        return app
