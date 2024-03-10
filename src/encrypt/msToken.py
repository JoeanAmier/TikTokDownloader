from asyncio import run
from json import dumps
from random import randint
from string import ascii_lowercase
from string import ascii_uppercase
from string import digits
from time import time
from typing import TYPE_CHECKING
from typing import Union

from src.custom import USERAGENT
from src.encrypt.ttWid import TtWid
from src.testers import Logger
from src.tools import request_post

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["MsToken", "MsTokenTikTok"]


class MsToken:
    NAME = "msToken"
    HEADERS = {
        "User-Agent": USERAGENT,
        "Content-Type": "text/plain;charset=UTF-8"}
    API = "https://mssdk.bytedance.com/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "fWb4VdKdBJ3/1u7AtgSkO0LmWPbiWZo7jauPIC9U6quTfhBnJEs1B0GBRuNG0lqQnBAUYVQyodx3Il3yfvfTkrDeEjMgoibDph"
                   "r1BtPSvmYPYRJtLuxL2/UuaYF0jAv/SjsjTxIehADN/+IdJ3D20EVgwKwTUIn9VcEJgZTF1MQTwdAQgYlpUAnjrOaofXh2PulT"
                   "NGr1wGBhplaBuRWU4hApsik0s5gd1OuvxZdGoxBJ5EKq560/Cvt40SvDQm1VgYFYpyLe4/V+1ti0kKvg7CHynPswthU77ai+bb"
                   "0p7RQW3UkhErQj+YR5lLpYT2A60Y5unpwnGIY44AzzJ4vgJNFucOoS4uGyPu7Y4wPhi4Drep1losms4nmp//AARSvs8U38L5Pd"
                   "5qAcOpIsnQvN+SvQCGnkaXjy8yDYpdZQLarWo1ZRtbCZ70cwB+T4qpmygqkuvnu6XQvqzwo3petpHTOtNIUnyqPvc3qugGq3/B"
                   "NFqGR2uOUk+2YGyMLIwFkmSKzT1pzseLnj6n+b4VDFcC9byhABxouNjdJqJnoHtipwlaZt5ma/NuHwWLKL34uVzuPSvviys0LZ"
                   "tcH+himoyugGtgAjz1uiCR841TnuvdA7peSUtWYYJSF+LqMUFQmt0zwXrrfIvqmeWxRQdOB47hXqRryqf1NUiyXYKikjVJOPIf"
                   "grnutpY7VjOqRjyfcnleHOqtZE+elE2oT39S7ekGo35n18nuPUnSoVfIeznO/9t4iSdAG9xXvM09hA6gZdCnCteaSuRVgWNggF"
                   "yRQZZKnMeBJKoAVET1xLl5lfua4h6ODY0m3BYxtwYibFppMnQj5W8RQyDCXUVyyN9HuRTsQiSFwIVDIp9/RZNWZWu7an8hftrg"
                   "cI+pU87Rm755nvQlXPW9jpuTN3G9Xni1/CsCQdz43d0G8fN6VlplmYwBp0jP+so1J9gmt5SJ2qMHHXp4fI+xagnqrHWDK1JTJU"
                   "goZRSvw08oFdJGrI3Muy6PyPBDKJs/njbJNWjo86csPPcTri6as7Fawt5nF1c1sVpCQDmQvJ2eYoQlSHFH6NGUjsJvbmoUSa2j"
                   "yYyD/22x0GWvnSWp8LVMuOgTW1nJuiP+gsNHTyfTyPlPqkx6fuuSCmwXltLkZjfZmnPYJvmMEP28BDuUCiw6Ib/1ryqTTy+Kt2"
                   "4iXzIGsaqatiecSwU0IGqHWveJ7Q4eAqHr+r4fmsDDOnImuRd/ApLvd2MD6vzqjKT/plgC8/L/J9dkEJnVl6X/u6MXr1la4QiQ"
                   "5Ia6ytuOSh57DUrj9TWxuIh+Pq6Egz0kpx2EKWIMl8vdsyL88ek4jWNEl9bTexx9clG/fWrH+YcaQHpgVfHCihLAYLLWBiQ+Ty"
                   "PuWQlFp0W/mTlY3GGB8rbTAla/pmFMZensgwwdUcfOV30BS7lZcU9R3AsYIrN/UTq1bz9+bTn0U7GLvvr0Dm5x6H5IMWI7Vh5a"
                   "0g4MopLVjjvySEy+3eStPKKJT3bHqZOGe90jG0J3RYXkeEJSK4w+0znVVjIdd+J6ZBZoiikeh8ElKjPop0vTA9SFzN/gr9+Q1N"
                   "PuwA4ewBiCPN4aTTZBnmjJljLnHsTL47XwC79JFZ/DMCHpiBfhwic+Y5YafMnwTuuYPoOPDy084UloUrAaEwsvTR/pyJJtmt83"
                   "Y08wUTR+DIWaYVTkukEXsIT0fyFaY3wVDAMXQuLLFd4KIhwrafPsEB7KBUn6AJBNGI8Dt8GVuBV64wWJajhy2MbygcxL95RCc3"
                   "kkjTPL4JmkZ8UHUNaWfqYoht8ZuNpalhfzHSjEPaNDtwyKBsqk2M8RUYucoJm7TvnhF2nqVGeRuOFA+uQSMHDMdNjbX/3F3Ijf"
                   "pjTGtYQEEzwMFBRk/tDf9/Vxv5eimSWFlEWJcPpsw0AUMwS0nOAv01zNDKtfgVRai4ioMycCPlS+na/ntBevVu1ZN1VpX7GHrO"
                   "zM5mv0PXl1v+FUNY9LysKgHuA8ePTY1jAeuZPLfJ5sgFG5wuSZpWOqDB+hwRhXqVV80dfHZUnqtq0qZbMvdfhszAjNVbp6ZxFh"
                   "Y7YaWwE8E9a89lHcQP7wSUWO16++7yJBg0F8IKxEAnVETpFAiZ8NDO6bEaNzHbCHBR1NcW5FSjaiO0zN2eEiLE7pWIQMfl2UuC"
                   "H4+nWo1ToT0v0YMf6JsHjWLGjmlgWTuLXE71H9Q0lYD+5QCqdtAKYI2bPnJ4/cTo+D2ZCpClDkjghW06cwHa0Km9pIVfbTouC/"
                   "8NEPoC75w/2wWjG0OO3XN4C4yQO2db4wCsVk3VaAKtF3D//Eoa2zGWOr1/JmFCbkkiAWis7JsEJ98N0D+jbv5KdTig2L6r95hl"
                   "BJ3oE45H1vbXW80+V2aCOlww2ewrDFx74HjhTTq/Z5ahjgMzPQv3VKhWjGa1hZmmRDjPsoRumTAlYrnGZkUcwolfgwhIFivhnL"
                   "Z6UgN9umrZmgu1W1Il9dZekmpTmyfYyyxP2+cCij/5knc7abwD6PNsyiukaw5wbHkSUbopv/ddyMGDPUIOckpU166Rn2iZiO94"
                   "Lc+Ob7h6J4HjMTF3gLvyiS3ec3ZLwbZR4Sqa0yvxGcVOEqs1Cowmszzdr++CiPre/qwdv4zAxjktjzExrzCInCDA0GuzkzFi2v"
                   "3QZN+Nxb6vy4Pg3T5qrdQNcbXaxU482gdzwPLCjfXEds3LrjU8AG8ssdC622bR9omgSBAStLY7NPS3qinCwDGOrAduLMTh62lL"
                   "r1ezW8JmOaAzRmxm8V3uxZsOWQj3qneoGkIsKKQ9ffeZuLzceu8ujCeEBkhenswKjoWXm2H6TA+tQOM/+SOuGkDRQSk1sz8CWz"
                   "2HEru47fh3fa6il9oN+Z5aeQssYIRgAeqP5ywFthVwwBDehm9udIr+G81jorR+a15gfHKZfsy043C8DNNhlLBFzvOVlqoWvgn4"
                   "TGx5hF8uMvVPhyK94eMjIC5/0Bxkm5yroylXz/qk7lWDqBrgjoXxNJOcwxl8P7+EtFT8EkSqfhigyOLTAN1VzJIyEORihlGDNC"
                   "YQowSp2qxyQR7capYLd8cEjEvqmvlfWx/ReytHYZWImGoddp10anbbmuynzkC95n/ReXHZMCKT1CjnEZy3JnsdjbQ9ttBPlU4u"
                   "EdMPZqHJEIuEZEtPe2SMNXq1QNqjA7qrKK3TtkbpC+2GyQiPC9P5f2vvKOT3sE1j5HFTqugSneQyoX6iwiesO4/L0PBvofmmYw"
                   "stLNrYCLhMFn8urNUu1koR8DxMEtwPuxEoJsL6DlsNJoxkdrdaVMsyAHFdM/gKDgHLR7K3t80lHa/PIEoAXqzYZrdwO0j0vvp2"
                   "p43cD0GPWjwd23hP+RCcksCwEUYWAZTEVWG65V/J+z1vO19uNf6jynefg9dT/XpMkoF17e7vR0jNWrOt18EA+CSdhu2UwzOW1C"
                   "BIrpNdloXQdI2H2FN+LisXgjJRETDraolH2S3Fj58BtZ3qu88g8c6nTZGPQ06gaFJJd0bRsSsSgGVEkLPsAdcH6Z8w3zu3iBW0"
                   "aftwCtZvcmlg2CNGOfkbrHpQB4/uGJ9h6E/M6C0K397DWGBhVMYjfwzuVANjjnUlEObExC1nTeIlQkqgkjc2Urox8t2k/qli6q"
                   "UEpFNvttCdmLn9+ZS4FCSCbPpUNuENO95C58Fuk3/0peBqFkqf3ysHXwuA8MIPmpLYCgdgtv3QZ9VERw3spFQt43siQZ5VIVKC"
                   "JS3TBrwEfMGJ7lm5NUyzl3nt5r6WEzDTCOY8B+hk8vZXYfes6JGzRzzjyqVxmCS+bohUzxiLGhdTqBmZVw/ulc6ndSK71vegRR"
                   "xJ0foTAlmcpSiZVr9pK15H0C9x1nXDk+W9i2tOSaoaN5y2rOWl9OIObVl/135ignY5E+ZHTDbBHeNxBmm5JR7W0XiC4LTF0V3+"
                   "pEjwVbkGi6kpEcYwukfG5UttlWfalxzv1YTcWhNOcKF1PFOpVF/C/E==",
    }

    @staticmethod
    def get_fake_ms_token(key="msToken", size=128) -> dict:
        """
        根据传入长度产生随机字符串
        """
        base_str = digits + ascii_uppercase + ascii_lowercase
        length = len(base_str) - 1
        return {key: "".join(base_str[randint(0, length)]
                             for _ in range(size))}

    @classmethod
    async def get_real_ms_token(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"], ) -> dict | None:
        if response := await request_post(logger, cls.API, dumps(cls.DATA | {"tspFromClient": int(time() * 1000)}),
                                          headers=cls.HEADERS):
            return TtWid.extract(logger, response, cls.NAME)
        logger.error(f"获取 {cls.NAME} 参数失败！")


class MsTokenTikTok:
    pass


async def demo():
    print(await MsToken.get_real_ms_token(Logger()))


if __name__ == "__main__":
    run(demo())
