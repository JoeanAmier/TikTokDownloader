from asyncio import run
from json import dumps
from random import randint
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from time import time
from typing import TYPE_CHECKING
from typing import Union

from src.custom import PARAMS_HEADERS
from src.custom import PARAMS_HEADERS_TIKTOK
from src.custom import USERAGENT
from src.encrypt.ttWid import TtWid
from src.encrypt.xBogus import XBogusTikTok
from src.testers import Logger
from src.tools import request_params

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["MsToken", "MsTokenTikTok"]


class MsToken:
    NAME = "msToken"
    # API = "https://mssdk.bytedance.com/web/report"
    API = "https://mssdk.bytedance.com/web/common"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "f310IdiueYEuoABxeOUGQmJgMDjjI8cBnWDP/EcJSHSemjR+ar3Lkpvw8amjZcH/IOGeIeig8HQOgRJEp2GjC1T6zLk8sHfwA"
                   "6twUSmdymFUwzPfjKrSKLrKIYIaiyDX2kPprlYaw7M2i890RVM5jXFvp95csvDWHbDVcse9YTncvo3rBRTlS/QPw5VqRZuYqH"
                   "/DjV1e0qFJNqo2JONb6mhBEgLjO73aHA5kdH6aezgUePbOOMNVtR8gArD5rGyJZ+FcLlBv7bfxJfHYqoNMEBbe7h2mENW0wVT"
                   "+jua4ZhOMyXiARUveOO7b/kHp8/00O5PZcXjy51IA5jSNFl7x2w2Ul2Vy5pot30afnU8ahNelGlJdf62fSsmapQdOqva00AAD"
                   "MuUggPoz7iEiumbe6gavWkCfjAIUHPhEYm1JWsC0zk+3hZonZMAh7kYCxuJXAt9056tjHWBYn1MIlZgFlcAE0Ry2s4nv1NFbX"
                   "Bj/2+TIIfF0W+IEsIJo1yKJ/4LPl4QLNU9FS/YW22evCldHEOCKyhAGn4wnZdKfuAmo87qPZeY0LfMTc6L5lj8oJvqo/DMs5C"
                   "K5zMN0GAUiaDxrW2pS+rYOVdbfnC5hED4bvHebrxutUddVx2acbJgfiMT58Y/cMBzGJPF+hk7cFxnA0MjUMHqnNWNgqID1lj1"
                   "s19vJdtLRBGr6H3UUslO9QE5TP8Alt9kK2FsXagWZxUnvtBhrGP9yqwZMdghiUyoiTssLJR6qAHtvmBxTiDTaKWlOnwTx/png"
                   "NSc8dMO4TsO8r++G+A+cSkLntG0B36e1+LqdUny7hJ66k7qNkGQ22Y3/65Otge4KkZyhZ6zl5fzU33mScj9y4lA2wl9lOM0nN"
                   "6C8Z8i3U3+95HmdI4uDbhSaYcCqe0BskegiLFNkTZ5NWd4Im9HMco1NnfU7Y+3N3I9f8L6lCqTo/A8K5HUn+CZPEPDWbDmjFE"
                   "88CGqh8aIEOPlF0OiDKd/r+uUVP9F0CulWLERRuBRvB/ZCzKWQQ4J6TBC5lBUgFX4VLwGnU0mUL/H+5+SUL9qMYmN5HZg5kNg"
                   "haRzhD3IKSeWUzu8weOEf6TiLqJv+mbG5lbdjCvFXI6BXySJFnFyBzDavkq4piGrld17JCLFacPizVolJ60BW2BlrK+xpDUsI"
                   "wmpvgr8pCbCGAczemifaFRGzya4SVCyCT0ccBEj0E3qqAqi/L7s5rOPIapoSKcfJW9D2T1GcquvIduG+5Q4mFMnUUMwWmogJ3"
                   "xPSl0GbfI9/svPE8U5LtdCl6y2cTqs64sTfJzSb/mo9bcVfncR+pzW9J9ZwDJdtOhi33NQA1SQFrJR39Vl8AdaWd2r6XkYSLx"
                   "y1Mhtcwq/0YovhCkasT2y10gqeopdI2ly5A1uNdatwwqCLUEsbgUQRzJfQXeC3ecLtBQovVvnSnviw4WAW9ICYXMmLVdNN4uu"
                   "tPwjaQvg1IAF3X9sbihWJQdQJZaPo/Ey+e9hju5FMt88h6xJ2oI+Rqztb/7vP1LYYpS5ZN1ANpjpR6A6miKXyxi5qIrmwkeON"
                   "FXCRdx0JOCb2zUDFyaLqjFqcvFJG1J5XXhqmKzAq8nRGFiSOsZHRxb1dsFdcK09rSISazjPOqTjeQxk9CtSaRVYjStb+S5/qt"
                   "tqEr2d1rwRZGW+RX5WtJ6v4NpRPAFRXff6XRfYdaaFYgl5gi3dtEnKpKqIZGkW4VjDnlTl34sNU2Ef4hsUjQUNzcji47x9J9I"
                   "3kan3Oi8lI0ELVR3tVQTT8twvtkysrrlTg15USy6Z4dSk6etAfd50D/qJi8GFE73h8f03+DMHUbFxyDyLp+oB2G3vUeYaDLev"
                   "4qanVl9BzJ/pq4b9ReYIRTWQ2VQFR58FbQKafKRIMuUga1T+mNlmgiwAVSnDmKiFSs+SIGrxdtS8T2oPU2eGpJGRslErd/g8D"
                   "ANb176sMoabs6puzWFsO1lSQSkxMv4TYLEntski/G56+HbknI5R1FlBsclWSskM2TgzSiyNFIklB6DlIL5siFxReG6a13pbFb"
                   "erjxcC90/Mnk7weCiptu+UXYWr7YGhV29aZCWxChGoLg216WTMOVrw7McgdHzc2me1/4Biu+4d9NNDbtFW33uC7TMXSa9EOc6"
                   "ZHEQkfXB5ELCP9UsiUp8N55cvmQ2/iP2eXT8uGw4mjBDGMENW8lK2y0bgMP2xtv2yz6MZ6yHmR8CzabErfd8r5ox+l2h1/RBV"
                   "STPFaLdumvjI2jg7g1dAdrBvm7Cz5NuzfkX5PWxgtTG+RkPpLaN0Qpz0Jl0z3yEHF6BybMFehj2XCWyVaicch499TDfdVlRpZ"
                   "Na4yPCgYh4KuKdz8UInOt4XLDNvoGH8Mz5CFVIXuQlF5s/4eyQFYZOKmS6ShouwX3C+1nZE1witwyArvLXHrxcrEYWn+B9vws"
                   "1W3N8jRNFCZyiTTua1tzoUBmZgnz7QH88KkCFDVyHDau/M3RJFWf1CV6OVmKzb/m5+BS+JQPt8uWzyWMjT+91XOk3P3eWqqYa"
                   "ZjKM2JpkgdX/ywN5rWHv2QJiOLTsaMXPE++DAyWMoYHCuA5ByCvj6X6zLW+la5UHKPFsva8SnoQi59h0mr9K3TMilncVbxPHM"
                   "z21THCYD/8zRoO9OoesxhJzygDZPcyGEDU6ZLr7w71eeIeboHvaFw9hwhZ5Z5d8v15RvkaADOiYSKZooF/NDvFJRGvGwrfGWH"
                   "2qdBt9PHC64eOrz6I7kYUgMIzUL1RPjTJ7d4VHCEB5cGxe8RnQ7t8L3gxpAGtd4Wdc993OWcCwlg+yWAcW2lVAsMyiw8wAUO7"
                   "+xUa3ee19nMPs9QXjeg6FCKwW1S16pGcZZmqBSG74jWTHf2y1Qrw/LfaoJzlx7cI18IrJdfxc5jlNjlRSsFPZOJuVKvebByqq"
                   "S5TPnokiJmtVSfO2WDhDgV5JZWXGkeH5Wxh9gxeM7bVQjrAr2sZLgznmH1c3Uv6AVKsmGNnOFK1jwLKz6qjEreiGkJJLU9quu"
                   "YJUp9XTYjRG9Sn/h4GRLTLZfhmMRxjbMuEOMDa01kNB+pp6VXAbz9zTN5k2BNLUY71DksGJvKbW2idchwE7gp75Hfs6azOAZC"
                   "H4JVGBvxSiHWdAw7rRIPDDgDIE606WTIH2Z/ZH/ZJoJhExTFLkSNx+JdHFygNfCTZK6JgJN5mJQgLKcrBneUno+bKnTpUbDHG"
                   "ouGtsRD0Cfj2lxLl3vg9T7Mjfy/1o0YBptJCjPK7fzjp2MA15OJQgYd+z29Q2cgKW+osQ9UYB76Tr/QSSxwjXGB7MhgzneXY5"
                   "10gRo1+dYi4X/YZEI8whRYWTlcPF6LTp6WJyddT5UTHS1Didj7qYCbaE7WrcYdWajXyX4urmD5P2hPIxcg9YwYMn9MMF0OLWR"
                   "EpOIjGDXFzX8eLNres0kWS8Hk4H9ov+Kiu1cQ8NrW5wC/qclriLnVtbMfIKG41S0AdbrTe3BteFzc8toAtLCfvrtW7O3lsitq"
                   "FV2OEZLawf9JWBmhFrb1YfEINehARC5+p3BdmNX/orxQAEOnVJz6WY2DXTY7jcMtyUcilUeGpwhXqvOxxqThDYgwJ2u/1hmoo"
                   "vgUfGx4ijHblajCb2wiGANvy9yMclGPLz5puQH0UbAfZnA/fg7BeuPYimEg6sOP1rXQ49+X/pPnQlrBueIuJIcRHSkNNHuSDR"
                   "is660VHIV1deYQVydQyFEQaR6B+2HGSFjbRy/7rce3Ol9HOA/ojf1nK/RBbhV9EzDXq4YkLe4wweQBsdC/EPD0workhC8O2dv"
                   "jckbymek/QCGIRt4UP2hP4IQoyHFgiTi0HmFGoLJvMUNbEFIbqa23q4sMmYonXK2qCZT9+/UOjvQQtpd/TuA/akiod7QZ",
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
    async def _get_ms_token(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"],
                            params: dict,
                            headers: dict,
                            **kwargs, ) -> dict | None:
        if response := await request_params(logger, cls.API,
                                            data=dumps(cls.DATA | {"tspFromClient": int(time() * 1000)}),
                                            headers=headers, params=params, **kwargs, ):
            return TtWid.extract(logger, response, cls.NAME)
        logger.error(f"获取 {cls.NAME} 参数失败！")

    @classmethod
    async def get_real_ms_token(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"],
                                headers: dict,
                                token="", **kwargs, ) -> dict | None:
        params = {cls.NAME: token}
        return await cls._get_ms_token(logger, params, headers, **kwargs)

    @classmethod
    async def get_long_ms_token(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"],
                                headers: dict,
                                token="", **kwargs, ) -> dict | None:
        return await cls.get_real_ms_token(logger, headers, token or cls.TOKEN, **kwargs, )


class MsTokenTikTok(MsToken):
    REFERER = "https://www.tiktok.com/"
    API = "https://mssdk-ttp2.tiktokw.us/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "3ZT3FXdGNeKwna7bgpdScOzfztRJweQycdcobgy3eK8JLvjXBMqtjNYGgXVPINDg9tBVhbqla2CJHkUa+c3Wcfeez08Ro"
                   "mo6xoftLad7Gigm1FNCJJPhURhuefUueudV8G7lds55beizy9R5cO4dmEflYWNxteVhdCZFf3UcXEb0Cuy7Xzo7//ZURA"
                   "hh73QFgpiNIctCfwFUbTHK216+gPgR7Vuld6+R9z2p8kEDboNmzTtIvh2WbY1vs++14ffHzOTYC12pJvw5D/levNE+kMh"
                   "7UrB/NBQ5qc8QcYyzkEkzKwpyQordqKB8emdvqdGWRj3PcVBUFRV/k81X5Z5IshDKNaepWyJaUA7Zij5dViHqMEMiGdKb"
                   "5E9jalZheRSmdrAEZz917iusUgOgprWOtKuDYKro7jF22m5i9SHJlXFKyYji63DwFQhpk4EQb5oDiHufopw5p4o6Ox2Qx"
                   "/Om3stKfBmFULjTX8e6kSgZE60uC02AAPSIPloAhqrwDY8ZXL3GwtyJRCQGwPtRbBcEx4BIvLQkfoMGi10d1sk7qI/cjA"
                   "CrZfe9XexsJZCFGC8fmwQ0HtwslSfg/5ttSdC35osiHYukHhX5skvEDuXPXDjT8TTI237prly99gFptB3EcUJ0dYRzUyb"
                   "NvY88zKlTHNjgTMNnsjP8k5Eo9EUtlW84yrcFfD4BslWQ8F3toc/nca4WQfYU+AcNN+T44tPyMGsO9ErwZKt2lA9bVmSQ"
                   "br+VBC9ApevHo1fJM3ouMNbFEWIWbvCnRXgimgOByy3mh6htpVBGIRB80It/3QdJA1XLgaiN3AeWv9CCgJdt599MBivVj"
                   "m6XucvYPg/JAzQR2DsB+42YDu3tjeX9H5KDKHqwhz+V+IAaA0t0tPQ8Nx+8LHNsZc8Fo6L3se52bMAYF9lqBs7PFgTh08"
                   "1ENeDvj7EuG1A5G5rPVTvQRCJBRPHpTaoXJF5tcuZePZo4FqT2ZIFe5Ujbbo6m+Fsvawn8XYKI9W8e4WmdTdLvyG/mNuU"
                   "ASkaobQVGnRRG7Dt7EVvuFSx5ej3ccI8QOYWFdrfCz8Znsc6s0RlwA2VS587lYut7aDKRP8Xp5f5KgW+4G75Y0/aCMSuP"
                   "Y/62QGFRuqdrV4Bkoi2mTF49nAsIfEmm0DZbIrh1D7op3bg0fx6JUoUeyNd1tG6H0GjGUNoHFl7UdxhZ7ffV2+Bs4mu2v"
                   "5eP0If/rR5m87iE+5/urw8gLQ37e64xO6zoFb3TII5Zjn/AjFYy7QR/zUVJQl05Kp9UIw/3E2oV27lJgYLtnaSc6uNGX+"
                   "iAv0S2dA4TKehYjqcqxKhM2HIr/UNA2crOq76dFhycHLJGO0Wh+3CKA11AEGvFPCFP7mmXQNxmSTmBB6ZqvL1/V5oMOis"
                   "DoobJW2KmFnF4HUsFTj9kN6BpYjCixHigsx6P75cbDIkjpcA+d18G4+F2HmEZC6uzbKIaNy9SKe7SR4bkktiA747H1c+u"
                   "+lyMjoMRWSz0WzKhJYCZ0aUGLSV1lZ0CUp7HH51ePoOk1dXVprhsmVKnt1VKu3bfncEImmFtrmxwipVB/OOU9rgWVrtk3"
                   "r43ou4pPsodFQtIvPmIWVLxqIT/6mEo7r60leqqW0reFd8w8b86PMJy79z7DlWvowgxJP9nsxNvK43bwO1rS0P8NhwIyF"
                   "Its3BzjZ1L3KrwhvekH6xEhL70zZrJHMtu2gS5SOaXNMdT3gMBnhRhtffLDDZsDu2K/CG28UjP3xlFZgmnhQ4wWejbWfg"
                   "EURhtGN5hUouXVAdQ+vPCbQY4TE2VnzvVZvBBYLyubaBc8t3RbAXfNOLm2vdOuN0vjiqTMWyvGBR+Jl1wIwBLUOEqRBnC"
                   "HH25dlQ/gyR3MYsG9v0Wsjz7ODkLJOQzfe3nYR+nhBNt02KW2y0YY6N+UkDOvuMpl23+c6UCiQHmbWpBDz4xCtDwaPd6U"
                   "pVHGbmZEjY3dHK1xyCIBRyz5yko5Hxz+/5ltXrZmwfAHvo4vj+GpjzHjNYDgZqvS99zXguLEPySIEmDKuDFg7T90dlF25"
                   "n5B2FJVOx71GKExiO0F+VivtDZcM9JedC/4LUNWkdr90iLaGcMKFk7ayZxjMB/zE216cVoxIZ7DnQwm78z+I4zwanQN6m"
                   "lICMQlbeBt45vaxW/9U5CSooRKYP5O3yH9g/XdKuptxXOYXrZiguiwZZEi7NA251qisO06a6PbyjIGubOdqEAEAfZdYnw"
                   "PIkc41CeIjs4M6+x+nT2oMs6mWJfAHRkF0zTvpGdp0ez5G+SW1mL7j6IZ8v7yLf6i+AK5+y0doA3OHt8sPe7Mt2/ksSBa"
                   "qy9ooUZvE0CEBKaiXst+7r6tBy4uaWMpSSkSX7vW6Uc3cMo0zgcj3gHtPWBIGSa0b2Mu1TxT/awtxtlC7IjHT4tgO88yo"
                   "cuKaQdpDSDl/+1Re7Q4GO5obE8SoEOoS2qUVkV8zdSFJFuzoNRsLgEDnRSdaYPtj0ROq9TMadAyZwduJrK9OzLp51J7X9"
                   "W0/LvmkFUSj2ut8DROVcXtl0l06rzbcP0AE17r/WFaYT4tfUwOjEwhIwd0gtG9vSiNaTxemogQwqGpcO94+JcoHo9wU61"
                   "w1sqyxqUohq9zQcvK1ZMdDLHKZlIFNuXJl/OlZjoGBILThwKN+EbxHO076/dJG5I6GIYOlgPJKmA7/3QwdmyuvvxLPXI7"
                   "smLLwA0ofpgC2sF0acZtXoCNfb2P1ZhN8PvfmIe2BXZPZ9cuHBr6RZeHVt6IEp230x//Delsx+C0/+g7x0wEeakGQL+5Z"
                   "TLkISrZ6QIoCUvim7AqvqNtZ7rG1CsX0f31YiIHTuOSaaMQpZwxqmVCo5JhaYkY2jGWgdwN62xURe6CKysvyTH21JfzrR"
                   "gXcEYpVg/VPl6MALTx2FAf9AoIsri2WXUzmXUsB0VK9W/z3fAXAZAnt/fm2aXYVp44y2708PiT+J8YzTSsVxdWMJYCJ+9"
                   "jLuomZUMRlPjdnJEvqgu/vYoN7XCzQM4Z0fY6/WyGTCO4JfuLMARJsuTv9qDXhuqs9kQu3Uajk5TMI7iWuPxgXtn1qOm6"
                   "USWrpvYaedRhm39PTnTkq0P+wc0NUsRHXg4qNB8voz1Uo2EWHCRBIi5QA61SBmWOdjS6MTNfEURMvGg4Rt/CVYqSZ9T03"
                   "jM4mreEn/xtyG3LmtKFKPDu8pmkpex6hn2truLCFgAhrEhJk/wenSbssAY/YPlg1EZ1eQVxvE4YpfwigS0psPyt8UMo5V"
                   "1FVmg0OAPK8LccPqvGra5BxIvnrT3I7mcRGff6V1GP7HKtzjBj9f+8NpS4eFqDDEMGRfZZS/XHul0+jSEdnlTUk6ccB+h"
                   "HVNzBk3VpEyLmJiQpNNfPlMGKKIkk0OVWQdQCVofGUzmjaVvxEBLqjgpciJDQUkwNud6Z7JTMysllQ6YFtovH3YRKqlEU"
                   "L4eo0kBR2HZocZdq7BF1CMmIWF2WRGiykv30dK+Efk39A4HW+kb0vtclI4GO9rh28AR4nEu8aoYIfKOZPAOcj+xJDEyfW"
                   "NgDyiiaVZ1rcnLvqGIHdkBZ5IXEAuOlQE677/spzi0pXzuZdUpLRsTMstNMBaMsNQUksRoeSX0T97PMmNULdUYCfnMnGW"
                   "QsgW4tPMQWH6i3ErOlN5F/5wwOD0J6uMxiCoZdbIXAv0zZyWrzWGaGsuC29MKmpgDQJ2q0/y0xfk+81qd+Ifa00ujovXK"
                   "mtBLyUYe4iHRa2jelOD2wlxbw14hLDhRU8V2xrxaM5dsqL0gi5IcRJHuCDf7PWz6pGVNcMgQwDfjFB2ivam0AqP2a9do6"
                   "Mlv7pl6vx7dGoNS6FFZ63lDUYtOqKq/qTcEkjiAN01rhcDu4jdHphX5ulh59L4Wi+h+yi+syw00j+mMX1IzS2/fuXJVSd"
                   "s2/Y/IUs5agZhy8ZBtW63KI8ve5TlLD6NPp3Tb+93hvZhVxQtNZNEtr8Lxs82NCMqB+AVQst5HwEODMoOVLCy90L3BqZH"
                   "RzLDdPZc4IIygLMAZ3o9EFhAY8WFfSXsIA6Ca8ja+dlrXwypSYmSSAbIbTdInWfljbedaZv+B+3waYmw/4P8oR1L6xWbA"
                   "6Lu1qYvcjADskrzLXTUOIoeyFyWKD9KZWK5MhpZKwOnTNRkxaHAHayNvyK+TxhIO4a5bGFchFrSHODq/MwGFCIB04Q8z8"
                   "mGz7GV8zV6IG0SoBkdVgYPPrZARQ/y699wvplsvyMcYYtOeQ8vUyIxyndRqrjuujZaZl4c6psQ4Of5sFqv86YcQwqzJTI"
                   "GUa3YLQ8wal9obD4ICsMZIAf7KvTUB9bminbWL4ohfbXPaN0y9mx0ljfn+/Aq07reymvPz7Cwm+ZffEoklV5a9+iPT8Vy"
                   "LYCFcVSQzSNppn1Xa+dgyC6j/ZfI9Am6dEnP1abhY/uywImPCbFqlfS4vYyl0yb9klyBdOtsoT9dzbM0IcaPEeqQixAoO"
                   "5fsb",
    }
    TOKEN = (
        "VQvnqAjMrz3lTcZuMS4FBrRj-TJojLWMn7xYNzGgaeMud1tQaSJ6U-6PzjgKsl"
        "-3tIj6fPCnkbhTo5ro0KtohFuHI5xiDakWVVkFRHhukCfWxGyDGCkrd79CoBvHWwxBKr5JpU_O7mEcH6IGX33Xm9rk9Q==")

    @classmethod
    async def get_real_ms_token(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"],
                                headers: dict,
                                token="", **kwargs, ) -> dict | None:
        params = {cls.NAME: token}
        if token:
            headers = headers | {"Cookie": f"{cls.NAME}={token}"}
            params["X-Bogus"] = XBogusTikTok().get_x_bogus(params,
                                                           user_agent=headers.get("User-Agent", USERAGENT))
        return await cls._get_ms_token(logger, headers, params, **kwargs)


async def demo():
    print("抖音",
          await MsToken.get_real_ms_token(Logger(), PARAMS_HEADERS, proxies={"http://": None, "https://": None}))
    print("抖音",
          await MsToken.get_long_ms_token(Logger(), PARAMS_HEADERS, proxies={"http://": None, "https://": None}))
    print("TikTok",
          await MsTokenTikTok.get_real_ms_token(Logger(), PARAMS_HEADERS_TIKTOK, proxy="http://127.0.0.1:10809"))
    print("TikTok",
          await MsTokenTikTok.get_long_ms_token(Logger(), PARAMS_HEADERS_TIKTOK, proxy="http://127.0.0.1:10809"))


if __name__ == "__main__":
    run(demo())
