from asyncio import run
from json import dumps
from random import randint
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from time import time
from typing import TYPE_CHECKING
from typing import Union
from urllib.parse import quote

from src.custom import PARAMS_HEADERS
from src.custom import PARAMS_HEADERS_TIKTOK
from src.custom import USERAGENT
from src.encrypt.ttWid import TtWid
from src.encrypt.xBogus import XBogusTikTok
from src.tools import request_params
from src.translation import _

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager
    from src.testers import Logger

__all__ = ["MsToken", "MsTokenTikTok"]


class MsToken:
    NAME = "msToken"
    # API = "https://mssdk.bytedance.com/web/report"
    API = "https://mssdk.bytedance.com/web/common"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "fWOdJTQR3/jwmZqBBsPO6tdNEc1jX7YTwPg0Z8CT+j3HScLFbj2Zm1XQ7/lqgSutntVKLJWaY3Hc/+vc0h+So9N1t6EqiImu5"
                   "jKyUa+S4NPy6cNP0x9CUQQgb4+RRihCgsn4QyV8jivEFOsj3N5zFQbzXRyOV+9aG5B5EAnwpn8C70llsWq0zJz1VjN6y2KZiB"
                   "ZRyonAHE8feSGpwMDeUTllvq6BG3AQZz7RrORLWNCLEoGzM6bMovYVPRAJipuUML4Hq/568bNb5vqAo0eOFpvTZjQFgbB7f/C"
                   "tAYYmnOYlvfrHKBKvb0TX6AjYrw2qmNNEer2ADJosmT5kZeBsogDui8rNiI/OOdX9PVotmcSmHOLRfw1cYXTgwHXr6cJeJveu"
                   "ipgwtUj2FNT4YCdZfUGGyRDz5bR5bdBuYiSRteSX12EktobsKPksdhUPGGv99SI1QRVmR0ETdWqnKWOj/7ujFZsNnfCLxNfqx"
                   "QYEZEp9/U01CHhWLVrdzlrJ1v+KJH9EA4P1Wo5/2fuBFVdIz2upFqEQ11DJu8LSyD43qpTok+hFG3Moqrr81uPYiyPHnUvTFg"
                   "wA/TIE11mTc/pNvYIb8IdbE4UAlsR90eYvPkI+rK9KpYN/l0s9ti9sqTth12VAw8tzCQvhKtxevJRQntU3STeZ3coz9Dg8qkv"
                   "aSNFWuBDuyefZBGVSgILFdMy33//l/eTXhQpFrVc9OyxDNsG6cvdFwu7trkAENHU5eQEWkFSXBx9Ml54+fa3LvJBoacfPViyv"
                   "zkJworlHcYYTG392L4q6wuMSSpYUconb+0c5mwqnnLP6MvRdm/bBTaY2Q6RfJcCxyLW0xsJMO6fgLUEjAg/dcqGxl6gDjUVRW"
                   "bCcG1NAwPCfmYARTuXQYbFc8LO+r6WQTWikO9Q7Cgda78pwH07F8bgJ8zFBbWmyrghilNXENNQkyIzBqOQ1V3w0WXF9+Z3vG3"
                   "aBKCjIENqAQM9qnC14WMrQkfCHosGbQyEH0n/5R2AaVTE/ye2oPQBWG1m0Gfcgs/96f6yYrsxbDcSnMvsA+okyd6GfWsdZYTI"
                   "K1E97PYHlncFeOjxySjPpfy6wJc4UlArJEBZYmgveo1SZAhmXl3pJY3yJa9CmYImWkhbpwsVkSmG3g11JitJXTGLIfqKXSAhh"
                   "+7jg4HTKe+5KNir8xmbBI/DF8O/+diFAlD+BQd3cV0G4mEtCiPEhOvVLKV1pE+fv7nKJh0t38wNVdbs3qHtiQNN7JhY4uWZAo"
                   "sMuBXSjpEtoNUndI+o0cjR8XJ8tSFnrAY8XihiRzLMfeisiZxWCvVwIP3kum9MSHXma75cdCQGFBfFRj0jPn1JildrTh2vRgw"
                   "G+KeDZ33BJ2VGw9PgRkztZ2l/W5d32jc7H91FftFFhwXil6sA23mr6nNp6CcrO7rOblcm5SzXJ5MA601+WVicC/g3p6A0lAnh"
                   "jsm37qP+xGT+cbCFOfjexDYEhnqz0QZm94CCSnilQ9B/HBLhWOddp9GK0SABIk5i3xAH701Xb4HCcgAulvfO5EK0RL2eN4fb+"
                   "CccgZQeO1Zzo4qsMHc13UG0saMgBEH8SqYlHz2S0CVHuDY5j1MSV0nsShjM01vIynw6K0T8kmEyNjt1eRGlleJ5lvE8vonJv7"
                   "rAeaVRZ06rlYaxrMT6cK3RSHd2liE50Z3ik3xezwWoaY6zBXvCzljyEmqjNFgAPU3gI+N1vi0MsFmwAwFzYqqWdk3jwRoWLp/"
                   "/FnawQX0g5T64CnfAe/o2e/8o5/bvz83OsAAwZoR48GZzPu7KCIN9q4GBjyrePNx5Csq2srblifmzSKwF5MP/RLYsk6mEE15j"
                   "pCMKOVlHcu0zhJybNP3AKMVllF6pvn+HWvUnLXNkt0A6zsfvjAva/tbLQiiiYi6vtheasIyDz3HpODlI+BCkV6V8lkTt7m8QJ"
                   "1IcgTfqjQBummyjYTSwsQji3DdNCnlKYd13ZQa545utqu837FFAzOZQhbnC3bKqeJqO2sE3m7WBUMbRWLflPRqp/PsklN+9jB"
                   "PADKxKPl8g6/NZVq8fB1w68D5EJlGExdDhglo4B0aihHhb1u3+zJ2DqkxkPCGBAZ2AcuFIDzD53yS4NssoWb4HJ7YyzPaJro+"
                   "tgG9TshWRBtUw8Or3m0OtQtX+rboYn3+GxvD1O8vWInrg5qxnepelRcQzmnor4rHF6ZNhAJZAf18Rjncra00HPJBugY5rD+Ew"
                   "nN9+mGQo43b01qBBRYEnxy9JJYuvXxNXxe47/MEPOw6qsxN+dmyIWZSuzkw8K+iBM/anE11yfU4qTFt0veCaVprK6tXaFK0Zh"
                   "GXDOYJd70sjIP4UrPhatp8hqIXSJ2cwi70B+TvlDk/o19CA3bH6YxrAAVeag1P9hmNlfJ7NxK3Jp7+Ny1Vd7JHWVF+R6rSJiX"
                   "XPfsXi3ZEy0klJAjI51NrDAnzNtgIQf0V8OWeEVv7F8Rsm3/GKnjdNOcDKymi9agZUgtctENWbCXGFnI40NHuVHtBRZeYAYtw"
                   "fV7v6U0bP9s7uZGpkp+OETHMv3AyV0MVbZwQvarnjmct4Z3Vma+DvT+Z4VlMVnkC2x2FLt26K3SIMz+KV2XLv5ocEdPFSn1vM"
                   "R7zruCWC8XqAG288biHo/soldmb/nlw8o8qlfZj4h296K3hfdFubGIUtqgsrZCrLCkkRC08Cv1ozEX/y6t2YrQepwiNmwDVk5"
                   "IufStVvJMj+y2r9TcYLv7UKWXx3P6aySvM2ZHPaZhv+6Z/A/jIMBSvOizn4qG11iK7Oo6JYhxCSMJZsetjsnL4ecSIAufEmoF"
                   "lAScWBh6nFArRpVLvkAZ3tej7H2lWFRXIU7x7mdBfGqU82PpM6znKMMZCpEsvHqpkSPSL+Kwz2z1f5wW7BKcKK4kNZ8iveg9V"
                   "zY1NNjs91qU8DJpUnGyM04C7KNMpeilEmoOxvyelMQdi85ndOVmigVKmy5JYlODNX744sHpeqmMEK/ux3xY5O406lm7dZlyGP"
                   "SMrFWbm4rzqvSEIskP43+9xVP8L84GeHE4RpOHg3qh/shx+/WnT1UhKuKpByHCpLoEo144udpzZswCYSMp58uPrlwdVF31//A"
                   "acTRk8dUP3tBlnSQPa1eTpXWFCn7vIiqOTXaRL//YQK+e7ssrgSUnwhuGKJ8aqNDgdsL+haVZnV9g5Qrju643adyNixvYFEp0"
                   "uxzOzVkekOMh2FYnFVIL2mJYGpZEXlAIC0zQbb54rSP89j0G7soJ2HcOkD0NmMEWj/7hUdTuMin1lRNde/qmHjwhbhqL8Z9ME"
                   "O/YG3iLMgFTgSNQQhyE8AZAAKnehmzjORJfbK+qxyiJ07J843EDduzOoYt9p/YLqyTFmAgpdfK0uYrtAJ47cbl5WWhVXp5/XU"
                   "xwWdL7TvQB0Xh6ir1/XBRcsVSDrR7cPE221ThmW1EPzD+SPf2L2gS0WromZqj1PhLgk92YnnR9s7/nLBXZHPKy+fDbJT16Qqa"
                   "bFKqAl9G0blyf+R5UGX2kN+iQp4VGXEoH5lXxNNTlgRskzrW7KliQXcac20oimAHUE8Phf+rXXglpmSv4XN3eiwfXwvOaAMVj"
                   "MRmRxsKitl5iZnwpcdbsC4jt16g2r/ihlKzLIYju+XZej4dNMlkftEidyNg24IVimJthXY1H15RZ8Hm7mAM/JZrsxiAVI0A49"
                   "pWEiUk3cyZcBzq/vVEjHUy4r6IZnKkRvLjqsvqWE95nAGMor+F0GLHWfBCVkuI51EIOknwSB1eTvLgwgRepV4pdy9cdp6iR8T"
                   "ZndPVCikflXYVMlMEJ2bJ2c0Swiq57ORJW6vQwnkxtPudpFRc7tNNDzz4LKEznJxAwGi6pBR7/co2IUgRw1ijLFTHWHQJOjgc"
                   "7KaduHI0C6a+BJb4Y8IWuIk2u2qCMF1HNKFAUn/J1gTcqtIJcvK5uykpfJFCYc899TmUc8LMKI9nu57m0S44Y2hPPYeW4XSak"
                   "Scsg8bJHMkcXk3Tbs9b4eqiD+kHUhTS2BGfsHadR3d5j8lNhBPzA5e+mE==",
        "tspFromClient": 0,
        "ulr": 0,
    }
    TOKEN = (
        "TxdpTz-pcVsDhVqz9nLZl5vtHpz_GX-iZnYiWDv_0Dmel-jA5Ix5WhKfoe16w6Yau0ljq10lozdji_DI7AHjs_Bf9sA-u"
        "-xOiNZpfrnCpKuXLFeAOxH3zQ==")

    @staticmethod
    def get_fake_ms_token(key="msToken", size=156) -> dict:
        """
        根据传入长度产生随机字符串
        """
        base_str = digits + ascii_uppercase + ascii_lowercase
        length = len(base_str) - 1
        return {key: "".join(base_str[randint(0, length)]
                             for _ in range(size))}

    @classmethod
    async def _get_ms_token(
            cls,
            logger: Union["BaseLogger", "LoggerManager", "Logger"],
            params: dict,
            headers: dict,
            proxy: str,
            **kwargs,
    ) -> dict | None:
        if response := await request_params(
                logger,
                cls.API,
                data=dumps(cls.DATA | {"tspFromClient": int(time() * 1000)}),
                headers=headers,
                params=params,
                proxy=proxy,
                **kwargs,
        ):
            return TtWid.extract(logger, response, cls.NAME)
        logger.error(_("获取 {name} 参数失败！").format(name=cls.NAME))

    @classmethod
    async def get_real_ms_token(
            cls,
            logger: Union["BaseLogger", "LoggerManager", "Logger"],
            headers: dict,
            token="",
            proxy: str = None,
            **kwargs,
    ) -> dict | None:
        params = {cls.NAME: token}
        return await cls._get_ms_token(
            logger,
            params,
            headers,
            proxy,
            **kwargs,
        )

    @classmethod
    async def get_long_ms_token(
            cls,
            logger: Union["BaseLogger", "LoggerManager", "Logger"],
            headers: dict,
            token="",
            proxy: str = None,
            **kwargs,
    ) -> dict | None:
        return await cls.get_real_ms_token(
            logger,
            headers,
            token or cls.TOKEN,
            proxy,
            **kwargs,
        )


class MsTokenTikTok(MsToken):
    REFERER = "https://www.tiktok.com/"
    API = "https://mssdk-ttp2.tiktokw.us/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "34t+6IAQRGtGe1FA5AcCk5dF4BPSdOUxHFrxQI/mc8lc6NeBHzKmffyCfYVR0/gmUQb1xgAxQoircKpjgKGVh/PeMOzKDC7GjC"
                   "yEH33nvZRoSd/BBSxV5dFRXJrx4eVr7YDIzc8Wob07R2N3fQB0cHugw9gIr5ZGezCgs8/utmiOPLVtnjafmzUzwnVqTTap6CaL"
                   "YH+3/enUnDW2BjIbsAVafxjIRITqnll6HkkyMAfEM/lpEFg5e8nMpNQvNePkOPcOzgCMLFsGXE3b7MUpc7wWOcHDeEk5PrboTE"
                   "7zXVhL4ltQ6sIOifa2RaK42zoebKCnDW3HxCyH/AqpROkLBTkBgcYdB3c3IneEkbZZWkzpoiq1181P++PMAY6mggLOLWDNPBa7"
                   "/KJhcGr7GFBWVM2WWnJHscE8fETUiqwBsVgQ5PaZvL5o3/rBPJqM4Nmb+m00BWeNemhfRv6xVgTtWb8eB4kbrQOesRnFdZjBOY"
                   "WtTFKWtr35x8pMzpwCN3cueSADXOWBeJPQk0/lPouPwe4AROlLQuSNvOaKSCHhj1AzzpQ5rl3ricyymxuCDl0kTVc7yzySaMgT"
                   "isN0F/qBmfNj+w1Y99Mbvmy4hefvjwhwDlCOmrTDiB4Fkk9q0Z8ziUrvOjl2dgfEruStmEXwjryi4klcxcR+uk82mSt6CrEijM"
                   "AgqsNrKKGjOi/WGnEXskDANEqjEms3Iy3xfLD0ywHaPwYzFOxmjgKO+XQcPS9+5V2pKRLQrqJIASWOQbgbOwUcysSEmzsl/vFg"
                   "H4NU0pMa6nDP4xknfIjyIeoUHJbjFsOSlcJUMTnDxG8wltmvyJ/e+idnAUybMugJ/KBMHHB4ruHS8USpo7kLxgje/KhyuD/34H"
                   "soFAEB7F9LEz1UHdncKjTPQjVltMRRc2SF5LrTOAdcz4Q5MXrwg+0FHz8k4LEFx1OOUREyoT33OPrACV8pCk6t5qF7UosrIOCc"
                   "gBWA2CyLd+/ap2C+86BNLbLR00B9suZJZ8JzbdvKO4Qd3XkcxraX9orFoEjlDiA/Jyvgw11B2mKcYKdq1X5/6oJz2x0XGNvwuc"
                   "PcINPPerICRMsTRZdel+dOnKMJ99RtkxNHHHyGhDUf3entFTumuG8ME0OK9eEhzSwRGiF5VUC2zDUzfKteKqlP2tSU0pdMiHGG"
                   "l96y6GD92mTSWrly8SE7P8tbluIe0OYuvXAWQ0IIK555CZ1GZfJjXlWIVIsFb1OyEfTsS1fRhKqXBYmwt1RNrAI90hNwMGXS+L"
                   "OAu5qIXO7SyHsxmtDhaRFtLfsBrREkiGFDoV1Rp1vPe5zkb8EVEP8vXjRD6V71JxrLl7bM1Z/ro87MDu7cVF6+bF36Mh3kJZ8E"
                   "z0rpmDjy5L2oKcJoixX32O1OAbgKHrdRZlxAebV7tQgNbhm36uGtl1ibbW6VuzNSuZB9DiD56GhptWuFurC1wGmg3FjYoQwSTT"
                   "A9VWTpfliutUTsZLfRG2ephN4epy5vURO56Oct4DoHR2PCHCToqddk9ODDmzA2vLUUTkEnZhxHcP8c0+sXRWHfGxbiw13mpKa/"
                   "k8+ghz7D2MJyhIhMTNZcUcUp77NA2WeRsfIFKGaPPzIBLejtKA2mshP8OMUPChhmaqNMic2rqx0DarcWmrUjn8XS63F7drGopY"
                   "2PN7+SDGi8xLjigyaxRX/cv0+Z6A8/sOFW4pkhCJqoh10YJnyOgRBHZ21qox1D+nZ9Sw2lpHzz14uVzw2FHXRqJSeHno5LrUH3"
                   "H0iQha6UGpKTUAhI8Kn1HgbQo/zsKDtRD2jinYhNH9NSHxj6Ojy0Xx5gIaB0KA/a/rTJcqlWXWpEFKLVsMVez7U3p4/QtMG05D"
                   "AFrPT4oX0ebjvH0UJR+rUO/CWsHGwjrXos9dE2TruKCtt/4yVpfaGiBru9qyawcjYuCgY6CWn44mPyUX9C/yJUy5cQ1SEhJ7nw"
                   "Id1ydS95OYFE/FvAotc1UqFKYUj6R6TAaGn8z3twad2JYg340nuBLvKAQV3bqky02Z7YouDQg2vyX9jEbDXThO5qxXoSsuvgh4"
                   "P1a84Au4AfW2qJstzAyiqMtkOs8N1j0Bx31OGUX+L9NtdM+rHVkXxCuVDoiJSWVUkhChEU+Mhqc83R4Nilh4GZxPAbv56bwVF7"
                   "jCReLImjsnauXj8e2g5WcC5QpfTkBL6Ii2fmUACgustVr86iB+vfLZGbNH4CrQb+navzVq+7yOO9RH0KHcM7H52+ziwc5flSfW"
                   "lqTQ/QO0rJ21iy2WnWBGu7Gz5Sw1u0QElO1bL/WuwW3jSNa05Yh1M0Htf0VJBiLXbCk//XfM/JSvlE0Rn+fFnfmAqiKgLFBlG0"
                   "U1ZFS3OM//y0pMEQYHFVmeBaFe2gjpy43jXK5p9uFtBiqyOzkaABI9x0fwS8VuIEmdmqu2AbXn4wJQJ/hE+SZMigU49K4FjNsO"
                   "Wid1xLrxl1GbZ3MLlMRRPNIf/Qgsd3pdB8pM9UyoaVEgTVqupN5/aGwrMGbX1mirq1uyaS6OFw7HyXp6bOzd4PdNqEPn05vCoi"
                   "lwVA35KTkIcognCRM9MHndrmeYlKfliKsyjSEizVcKm9d7Kk89lFqVehFmxjLkxsYwoEr7U9ZuHnkG10mRlIUO5dMA9shcFYac"
                   "hZ3jDpi9WoM6iaEuFD71k9MGC0lzhR2O+tHIyyXGO8C14/xB7PpFc/syo/7wC4LIXAXQn1zWzbCx9n5aBRwyG7ggtlKdo+qWmF"
                   "9+x0+2Y5BF4BPnGcYnPK0UTWit+9/jpP2HC6MeHLhPA8BcjYcFKhUA9L387U3qIkSiAGbPXRTYoso5n5VN7A93r0lzdwayCnJP"
                   "VtrFwICXjHPw/ySzO02/s/F6xlIqE2h8ZsFVRL2nHJR6D8OXVxvXzrULrw7BITPcVcUyiZH65WuDhDSqhDsM8QcgNQngVqGRAL"
                   "5TClHuq4NzslQP3etXsbY8TV75nvoo3mHTzoWBKBYZNGRWZBHUhG1PmWBzr9aczuHYvOeH0dWP14CKmg4bjgBwKsBBewmofmz4"
                   "Sm6BNkxF+mnZdXLboqijcjXle3uMyhAHW5mHEhrDvGbhC7QcQTVPdbpgIZrHtQUdj1N6phNTYOmDxkEIh66T2kVkCKdwu51Stm"
                   "V7RqJMv5lZWNmHFnj/e4+vD7HktDPtU6O8BI6LsEzVUzgwNMiioceDZaK2XsQ8HzVOhR9PsSfeYoEMQc/myIeOup+CtZZkPJrx"
                   "e9dx6IEypaFrKADAyActSW49GdjubMo+98L/8csDz0oxRxfIJRy6zNmVAQ8zQ44Gf397sVG5Vq9hm+iLNDM3E8PXIeNnjj4TGG"
                   "ArwHqvVy9iUri5kycjmZh4RujGXg2ERB3s3k6Zmen/ugO3PIO/ZglOk8cAtreLasoCT5wwpZ11JuSEAmuGZPiSEPB8lzsB1ESh"
                   "UZ2ycVGclhYATqaz8mld/YhZS75T4lwlmiCoTnOIUp3KHbwVJHb6GxmNMu4cq7CYwNSdrG7jG6Zrp5w7Mx9Vp3LLIUBsH3kOOy"
                   "gRNCGxZ7tmiABzJlA98GOdzzF2HwrsrsCiF2R0J2Fpud+J0qQdD/O9NRH8iU0Mae+WYH98tAz+hMEo45UBZBPZ6ady+Kr0FyT1"
                   "CPsh3pnF6R+C73eeOAwEhaPMAoCp8aov8ynaAikh6yhV9mbLreVdByKNL9oOmq1yEK3awk4+dnQMfzKmAwxZXEsNApMBYoeXy8"
                   "cpJJpVGMUJBuZSBLgCGcAmJLuOby93xf6YH5NcwmgjRuHrF3AEl9oaFvG0TEUyK3MCF7vuitDPHDZGl0N07A4YfsQLhcja7pXO"
                   "fRUIh5KVff+nLLyq2LLqO4YKGQM8Mxj7fyy4k6SYN1FNUkeXDOtbOeOVcd31eMzyfePOpForEq9dGdISVV/KZxTkK+nmvqqHYB"
                   "+u0/MWRMvfw2RmKKJKzGhYT4T0qangh33sMGGLDtrg0fm+c+M7jpgRHKZbMhmfAlL/lGVtmHzy6qa8/xho47CoxYQRjXub3LNB"
                   "h1/pX72zP3oTGJkbfo+sJaOPT3fILydGQR7zTIw7CYaVNwr70YhJ8odStwSVbhNKcWNtKzYpZCXaySMQ0hu64wG/GY7YBU64v/"
                   "/rPi0ByRVIzUjfmLpRJRCxbW13xzjzc4e2PaBzFHFHk3l3y7MFjQS8ntfjeMTpCowemB7AXBzTbL+ZSkS6wzp2rHrXXl9s+rF7"
                   "tVxSRBJPXx1wZVevJYYyBhu/fPxWrTFSEeZnP3dOcU21xTxjd75mSoW4nn4rDOix2I4Hu2t3R9IVsdv+xhsoPNHmjM4rCqTLSW"
                   "xkB+DOv/tXeC7+VxET4bCWp7RgQdyy1QJfbO9EF0GYqC3iYojyXRHsjDCe1ThiEi4rG/HcukHrP40YECkvfn/pTDn7xJ1okMTZ"
                   "SsxmrTMeS0zjtnhIo+BE==",
        "tspFromClient": 0}
    TOKEN = (
        "tWQyeNlnPlknDEh8suUhZQhOedOgAgRyQJGp4rCHrxTAlMS3wk9xGJ_Wrc2fgkPRVzkIr8fJw7VTjFcQ7glTWBCbL28_ptAMDlD1jI3a"
        "ZtgbaTxz36EXh0eiNDKGzI1PEweGi6we6L7_z7gvKoIxRWKm")

    @classmethod
    async def get_real_ms_token(
            cls,
            logger: Union["BaseLogger", "LoggerManager", "Logger"],
            headers: dict,
            token="",
            proxy: str = None,
            **kwargs,
    ) -> dict | None:
        params = {cls.NAME: token}
        if token:
            headers |= {"Cookie": f"{cls.NAME}={token}"}
            params["X-Bogus"] = quote(
                XBogusTikTok().get_x_bogus(
                    params, user_agent=headers.get(
                        "User-Agent", USERAGENT)), safe="")
        return await cls._get_ms_token(
            logger,
            params,
            headers,
            proxy,
            **kwargs,
        )


async def test():
    from src.testers import Logger
    print("抖音",
          await MsToken.get_real_ms_token(Logger(), PARAMS_HEADERS, proxy=None))
    print("抖音",
          await MsToken.get_long_ms_token(Logger(), PARAMS_HEADERS, proxy=None, ))
    print("TikTok",
          await MsTokenTikTok.get_real_ms_token(Logger(), PARAMS_HEADERS_TIKTOK, proxy="http://127.0.0.1:10809"))
    print("TikTok",
          await MsTokenTikTok.get_long_ms_token(Logger(), PARAMS_HEADERS_TIKTOK, proxy="http://127.0.0.1:10809"))


if __name__ == "__main__":
    run(test())
