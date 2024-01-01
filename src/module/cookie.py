from re import finditer

__all__ = ["Cookie"]


class Cookie:
    pattern = r'(?P<key>[^=;,]+)=(?P<value>[^;,]+)'
    cookie_keys = {
        "passport_csrf_token": None,
        "passport_csrf_token_default": None,
        "n_mh": None,
        "s_v_web_id": None,
        "sso_uid_tt": None,
        "sso_uid_tt_ss": None,
        "toutiao_sso_user": None,
        "toutiao_sso_user_ss": None,
        "passport_auth_status": None,
        "passport_auth_status_ss": None,
        "sid_guard": None,
        "uid_tt": None,
        "uid_tt_ss": None,
        "sid_tt": None,
        "sessionid": None,
        "sessionid_ss": None,
        "passport_assist_user": None,
        "sid_ucp_sso_v1": None,
        "ssid_ucp_sso_v1": None,
        "sid_ucp_v1": None,
        "ssid_ucp_v1": None,
        "csrf_session_id": None,
        "tt_scid": None,
        "odin_tt": None,
    }

    def __init__(self, settings, console):
        self.settings = settings
        self.console = console

    def run(self):
        """提取 Cookie 并写入配置文件"""
        if not (
                cookie := self.console.input(
                    "请粘贴 Cookie 内容: ")):
            return
        self.extract(cookie)

    def extract(self, cookie: str, clean=True, return_=False):
        if clean:
            keys = self.cookie_keys.copy()
            matches = finditer(self.pattern, cookie)
            for match in matches:
                key = match.group('key').strip()
                value = match.group('value').strip()
                if key in keys:
                    keys[key] = value
            self.check_key(keys)
        else:
            keys = cookie
        if return_:
            return keys
        self.write(keys)
        self.console.print("写入 Cookie 成功！")

    def check_key(self, items):
        if not items["sessionid_ss"]:
            self.console.print("当前 Cookie 未登录")
        else:
            self.console.print("当前 Cookie 已登录")
        keys_to_remove = [key for key, value in items.items() if value is None]
        for key in keys_to_remove:
            del items[key]

    def write(self, text: dict | str):
        data = self.settings.read()
        data["cookie"] = text
        self.settings.update(data)
