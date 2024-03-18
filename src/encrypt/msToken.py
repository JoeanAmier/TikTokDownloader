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
from src.encrypt.ttWid import TtWid
from src.testers import Logger
from src.tools import request_post

if TYPE_CHECKING:
    from src.record import BaseLogger
    from src.record import LoggerManager

__all__ = ["MsToken", "MsTokenTikTok"]


class MsToken:
    NAME = "msToken"
    REFERER = "https://www.douyin.com/"
    HEADERS = PARAMS_HEADERS | {"Origin": REFERER[:-1], "Referer": REFERER}
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


class MsTokenTikTok(MsToken):
    REFERER = "https://www.tiktok.com/"
    HEADERS = PARAMS_HEADERS | {"Origin": REFERER[:-1], "Referer": REFERER}
    API = "https://mssdk.tiktokw.us/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "3ZupDP37y+4Kyc0U9G3Mh/CMaHlAUVC/kX18BspqRG+ISe8G2GZkbPlm5P2YzanhYaeT6u9AKB9BX2HX20SYpgfwea7fmUysF"
                   "lqR7HyWZKpfZTeLvi38zog1p3slqQ45rNrzHWh2HuFxuql6bAGYFHhFC6Rvj8nR/eCLYC62AGEH3WdQ/VLESxzeSAHqS5wP1b"
                   "uBmreS8DtIMssZtrt8YQRgmmxH+6hZqut3WLDtImFnz9YISD8A7MUFZ9Djti32ny4L6v70R9vE6DlwJ0SJDceZgI52FiKADJ4"
                   "64qRRiuUBrVdwx/8+g53tOKbhHOPNEi/zUmqcOPrrjXL8OnHBis6/G7kkE//LMRPa1LtBfQUVeSACknbl+wycWBo5TXbir+dH"
                   "Qxe5BI94CnibgUo4QnK7VEebkAJPwB2T2LiyfIpn5BCJQGaZJVAahTeI+SjTlsx7Hqtq6ECahAc5VQRJsGDI6XE7DvVKDOGAN"
                   "3I+cAeEksuCO7o90F8pT+xK9QuKUW/0/etSSDk3Zw+RL9fG5KcRldnw9zRSynGwCnJigxFWm8DtttFeI7zCnM/+KSppb4rJ8s"
                   "gw2YDQ113OroCjpRcZRJCa29mj8CiBAMGj0NWtQvoFWQszQd3ilBlVHAAO4Ci4GEyjO+XtBOOGYqjCCWZElhrwrFL8f2QTaNE"
                   "aNsXsDNWPmdQBEuHhx2iFFU0/e1uJ+AKVSIQh/b3+IZE3/kJPMMVuF0NFoL5DQnUJfLhmdhZV0QHQr1tvJoQr3E+bOtNElKmJ"
                   "wyZUyoCYn4ADWv+sP8rZTMcRoFka7lqoKXqO88dcvDcmReJtFbXe9TLilWpRxKxwbD2q6JgNPqSk2ZRlynfZVVVmu3wG1wxZn"
                   "1mAxTlPMR2VQvPRkWH2iN2nuftP4BPleZBvfMVXU9tTPxNpl72yVYGOZQtl3AGwttCJ40C2usy2dfmXahZQbRsr8QQnBLmloK"
                   "r0nXqlkrJoKVYVJArOlYR61Im2yOHVOgHw6vyvegFtK8Z3wkvr3tzj8OpxqjIj4P9YQwMjudVn8q/8m3zDKwSL2+1NDsebSHY"
                   "juTyeqtooaJChEu1KkGwaD6hZxlGTyKpnyU4Gwa6OVtHTSv7Z7Zugy08ehYP07/5lsccdiDVRNg2doS54j9evmfVumBG41iIP"
                   "6m7xxfcnTFrkJa8rtda5DaBPiWcd5yfWzhW9ab3u55SGN1/pq7VC+MAoSv0LUEpCCksRMhay9FHFq4lxAs2hNW1L5pbXkmx1y"
                   "H5AIaWXDLKu+qXK2WcutNl+GGDJJvmfvilz3H6P7Oic90ts8AMMptaY6I+znzUsTYmRke8FR80Ioa8Uenl1j/U0QFOnaeLwrj"
                   "+j3nEr3mL/2ibdqsfG0tpM+yjFePOYTkiP9Lh2S0zwk0KpEtDF9O2hDZAZJu7XiNg32XcYKaq6jjfyvnbOldKnJ5RpZD68xyy"
                   "LUSYXW0P1Axd85xlJHU0oT+S6q6GnYAEohU3dGWI9yiTEjtJ1b5PiLYPz3rxMGwXVKcn6WNWe9wugUF2i2DwRYt5bjuXCNkOO"
                   "70XOS7xbJlQpoCK0F0y38VwF0oEyFY9GG2W2ZJa6gHazqBMniVYetJqR9PwaGj7Z3rNRuITu+yJYNH7pGSbLUucg5tPqrttG6"
                   "TBWUF1OZaq3vpOiZoHniSouUJMwUCJ4DsPHvK1nJh5FSUsbUQAtTtHaCPYK4jTIJY0XHo/uqNe8bMBCzCQRrWKSgvWOYKBnyb"
                   "lScGoDMvZnuZG+I7DFa8bRdBmbwCW7cDhlT0wRobax9ADggpG9yQ6b0lMJ42MtR/axFpusCYF1dHTywtos8+2+Refj1C5FHWM"
                   "6FIYBCSIjS+SXgHYm0nUfM20oMg4p4C4YnGcuTeU5vdNdsc//YSN9ivatjzMMQ4g+9upjVMlOJ57mDlRKnZ6bvGc2af4qU/kD"
                   "Nj3FN5VntlLvInpyFVz5Ytik/TNLalzywo+o5sYsFk/RlnAwyoSsfMFdZnEATnHTF+IBI1KNjkmOEC4MMnXUtQr59DEKgyUUO"
                   "dKUIoGDOCS5Onv4F6dcw6CGBWcA8+f6TTQ48fsHd0Qvud471+XaTLHJK42Pwn1++XmDTvL0cywadk9WbzT9arlX6uIC+K5FWL"
                   "YqaYGB+jgakCTVyy1Vh1Lo60uR6AVjg++vF+2OuiFmPH7eXD2YwECYbh5ngGFBrF5Qt53GqWCGXi/PX5apDJDj9HZ/Kbadg+h"
                   "bjJQmLX/WVq1LfiRZlT9KTTfOfDdIV6/Z4b0UKLFYnwibAp7Fl4XWi6NGhLB7p93fXM9MjAK7az5xhqQfwf79o2WD1hB+n/A/"
                   "SOPU5uqUYib+j9Pv6WxekJmKRq4uwPrvwjtWVKsLQHlNpY9fl/sGuE692IQaQ2IiWdJ9R4D0T53yv9WZ0BUue5YNoo888pVAt"
                   "X211S7knFUxqXMjtI+XfgRu/q4IusDOwS1tFQrnI0LzzZoCMFih8q4lh/DmWV4K5Qwl4n1dvUPqsQU32pf0lKnEZUIZwYg4iG"
                   "8TFTUh6ki0+lCP/xX6kL5MfCLPRcOLfIBglLFQph+xVjZvfhPUeDyYZwamS11Nv6N19Dq3nBhyMia2x5UwxHoy7Lmnj3y9dFk"
                   "D3bNa3hgo17u1LVSmUZR0kUIj8ACAkAezLxTLe8LdOkW07xGeZekWYqmchSs2StUaA3poBf/KQn5YwIOZRxmAEps3yZ55Wceg"
                   "hGOVMAlXZtTyBMWufGaRPEFUPbdo3BS9RWehau4nrQslfio8r1+6rXKvCtd/E3yRKzZqTaglGXwVWMwEDLMKQnDZSnmFrSyb4"
                   "yFVlExhlP9FsQWQyM0VAE6seHL55dKtrceUWtWCYVahlU9c0g1eeK4PR5cxyG99EOKowFhJYXlTS38UlefpEXNhjeExeT5hgh"
                   "k56vZiqnOpNcvM6hOATflZem1rpKA6nt9V2reDTX+A4V8xHi0gxZU/GNZeT9U/A7m7RTPj5Ix1xoh/BDF3pUUpjSK1mjZzjzi"
                   "tJqmJTLS6bKmpb87Jfm+b2RmHPnsF51uBgWsVa1ZHM9YscveEdHOPX0EmOZH8WIwV2JAf8h+n8REuxFTeZe9odGUBB3haiA40"
                   "ATwy8D9cxDLEwKkTFBEOrlKB33TkqLtE6d8cMRInPcxbIva7sg+P/Odwcj5reLEkBTnbPaEexjPOHGvV336VKFr4XNgyAO74d"
                   "CgyyVEh+drf3t8u7ZfHHfCpf0tQnNK9wnzyd4O77E2BsllNY18EGyuw9kF7eWXPwlUJUlDVtGMO0/QzQYeXq29h5h9nEKH/GK"
                   "vJ6V1ncJ8exlP6NYt4bF+QVbBJNQ9LwKebLmLMLImi8JmpK9qBNwHXsoJWqwAIRvFPt4vOMISRqFIENK0J0FCfx7Va7JqKLsL"
                   "wpz1obUOJksFUdljivum6MhpZlwuGJxKqZiW97+ik6YP1Dq43quSIRBYp1rVS36YTRRlqYUS2ana5TiKBYQ8OheNruzQGj7ds"
                   "NNJqt94Nm/hpjOOk5Q7tggqruCgYiLHQ9nz69qcrkW3Mxl1VvrM5kmv1HCafqyoq/VjgU05M1sksy6rwp32gft+C/i4GN31Et"
                   "JkHQ3ZGXRj/RHCdDD+VKm0E7QN6HfTk+ZB6nUEDbmTrIXfYxyMh4jWuQVhWKBkLHWxyuvrAIMFnQ7x2XRdcDKTXJw+mLOr02G"
                   "ZvfuBRInG5vVR47jbbUw1+8DiMdgPpNP7ig9OfDkSmCqMI9SjDN6+zOQxm7rRnaCOj+RO+9MzNXPLA0V1a0WH2xv9YV/KKSXu"
                   "9DS8MOpXkKKY5MWDgzUEB0TVX5/zfVKgNDiN/BJL5hoJADMKTIePWhABcv/tHYk1fBNMiHHgQLZ/ui5+VP+MN4ESDk02UEigC"
                   "uD0lH4YEk5gLC8U0uMJJFiS0BDI9e74P9RMr3OeITTE86Tga9PEkvxYL+AoggZBjkJ0AFdgzKZgiWpUEZvTsOAVHkPcjqzql9"
                   "87PaNEiHeTWd/aBYT4ZJOq5Tiy0jDxJq1KODjVdzUkG24Jygr0KTlLu9gxPZeL/BKy9k8cnHFXhs9sDf4YvWFeCkZ3XjUN0S8"
                   "MDEkCSY1lh4mZUrtmAwiLjs79aVRp+Z2jCkf94AkkT7lqQG49mJp8Hi6QcUM+sYyHZonWFtRH6Nkqob3GQ4JIXmKre8aQD0a9"
                   "PWI/NF2vWcfk33UanMAx/ltDJX85n5DGUYQx1sf/Yff13j8iSa66QJk8Ox3uDTs0ZLpcoqTR8cj/xM/cqiC25uuW/OLeNwXJX"
                   "8HHAd1/fXiIDXQA89w/yAc9O1TSsgNY8dAZYhoRa7FCdr+SSYLdJWEXq+cMyka6Xb97qn0v0jAVyeM7ZSmo00/fGrsQTrhgjD"
                   "OorzfstHkCsyc6jI7WFXoU2X1jvTDDdFZa+j2kaIpSWvn5SOl5N4viverF7FDtVFcRL10cWSQWcMrt6vP8R5qM2fC+0zwrBqR"
                   "dcB1GshBV08YqJvXYY83wNIPCwFqmO/9NVm5PqNAEPdlH8WPnk6onXbwenFB1J",
    }


async def demo():
    print("抖音", await MsToken.get_real_ms_token(Logger()))
    print("TikTok", await MsTokenTikTok.get_real_ms_token(Logger()))


if __name__ == "__main__":
    run(demo())
