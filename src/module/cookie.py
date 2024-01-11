from re import finditer

__all__ = ["Cookie"]


class Cookie:
    pattern = r'(?P<key>[^=;,]+)=(?P<value>[^;,]+)'
    cookie_keys = {
        "n_mh": None,
        "LOGIN_STATUS": None,
        "_bd_ticket_crypt_doamin": None,
        "__security_server_data_status": None,
        "store-region": None,
        "store-region-src": None,
        "my_rd": None,
        "xgplayer_device_id": None,
        "xgplayer_user_id": None,
        "live_use_vvc": None,
        "dy_swidth": None,
        "dy_sheight": None,
        "bd_ticket_guard_client_web_domain": None,
        "d_ticket": None,
        "sso_uid_tt": None,
        "sso_uid_tt_ss": None,
        "toutiao_sso_user": None,
        "toutiao_sso_user_ss": None,
        "_bd_ticket_crypt_cookie": None,
        "passport_assist_user": None,
        "publish_badge_show_info": None,
        "s_v_web_id": None,
        "passport_csrf_token": None,
        "passport_csrf_token_default": None,
        "download_guide": None,
        "__live_version__": None,
        "live_can_add_dy_2_desktop": None,
        "volume_info": None,
        "sid_ucp_sso_v1": None,
        "ssid_ucp_sso_v1": None,
        "sid_guard": None,
        "uid_tt": None,
        "uid_tt_ss": None,
        "sid_tt": None,
        "sessionid": None,
        "sessionid_ss": None,
        "sid_ucp_v1": None,
        "ssid_ucp_v1": None,
        "pwa2": None,
        "strategyABtestKey": None,
        "EnhanceDownloadGuide": None,
        "__ac_nonce": None,
        "__ac_signature": None,
        "FOLLOW_LIVE_POINT_INFO": None,
        "stream_recommend_feed_params": None,
        "bd_ticket_guard_client_data": None,
        "home_can_add_dy_2_desktop": None,
        "tt_scid": None,
        "stream_player_status_params": None,
        "odin_tt": None,
        "FOLLOW_NUMBER_YELLOW_POINT_INFO": None,
        "IsDouyinActive": None,
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
