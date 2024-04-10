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
    HEADERS = PARAMS_HEADERS
    API = "https://mssdk.bytedance.com/web/report"
    DATA = {
        "magic": 538969122,
        "version": 1,
        "dataType": 8,
        "strData": "fX7AYY6P2v1R7M6styZmpImbWwNJkUwesmlDmrPs+S9g2e3qhK/jyZRqbYs0iurJTnCJe29aDP9twJx+CT4oWFwpnSE7+OIpu"
                   "IXWsXaFgTlPmpMOBmk67cIc8RggvHkeb0+WCBtRLsocnA/1SjQb/cAanfTkW9O1ZZXZxKRPNsnvfjFRnCRXxs1jy3nxCM6r2s"
                   "lK0KzClCyu8MzAdsZ3LAonHMGF2YLozQ+jW1K5NMlOnbVs/jmaU/E16i5yYTDzUKaPf1KE6T8DhgLQ9Y1iHoGVQGqbn0oV9tR"
                   "v3aGmiHAW6s5V3GN2VYi8O1uhbubKQd3QWPF/v/SwnUfMiwxTzN2ZkI5tvW75r5qXgSn1UavExcp+l6Xvbrg8ne43YmNNRLfj"
                   "Z9ICObuk5ntV07wACyM481jupNyZZTzex0upTU61Hk2GJYim218AqHE7PMOUm4dN4Nvu+7IRcfTuJGayvRD5IoIovTmx6VJF7"
                   "9tpwteC2q+AQ4RMej+w2VV3h3hLK/lqm7xBFLCjuD+qzstKuA7yGznOX0IqQt2CUPXaLC0IaB9inowLpLukKdDZINbbaJgcHD"
                   "OnsBxrMqLBGy86iml1nOJez4VhiPKYx3qG/C3eaGRDReePeJGpzF4KIWNg8mmLhxJ2CfSvkXZjW9vDh81HK0Q4tBTdU/5fInN"
                   "LEYi5dMtGYqWhhFwUeq/T8tS/Wpj7DZedcS9TcDdc7ajyMq1afMhmiRXM5381fXoTqNB/CvcVZr6Qd5zqYFAsxPWJ1uk/e9dQ"
                   "tJGA7VgLRR8MGJAFWcdsp7U+MKBW2WT7tt9N47h8CoQihjFiab4z79j/amfFn1aZMTt/Wesbs/R2n/ELKno5tfer3OX6sMG2J"
                   "EGiZPLxh4rN6DAoUgC3B3msmJSw7HGt1uj6zcRQ9Bltvc53bkC41Ww+RwhSbDS3Xn6D7uXFKUDwngdITN015hElc6bBLJP6+n"
                   "sRt0bP1aUt43+ZMrSPPO/7MQxQ6VdYA7hwRvbofTvaQgZy7Bn6Uer4ght8rAoZKByaiNuhhV/UNCgc9GQHiPNO8OiNv3BkztV"
                   "SxirrZRxPKpqZw+xsEdGrawoadrjJgMuZy2UlNIRv9EGEh6LKcO+cUdx8a3D4Be8Xfhie2HjrNYMKgdwSu1T8XlUTqYT/ODHl"
                   "4IRw4+HLn/5NmVCs/niMa415jBBnLnXRj+sIsHYIFg9DRyUDN7AUwqICe/aMC4kqn/avAzJzelUN28QKrwcNc5A35eoWuCtwn"
                   "5SkmxF0FyEJiY+t5r0K5dZzE3K/V+buVowpEvjoPGtgkzLnykWri9Ylqbmlsd+bOTEdY9NvXuuII6gd7uLlC2AAYNt1I5r3IJ"
                   "6/xyQEs52aS12jP94sAgTkot7QX43WK0Kc1hgmW6raaaXGnD7DOIrvhZ4adf+CStWhcef4ILzBDWNiYBbY0Nq6ePfVjcd7vY2"
                   "cqyaYgTxUs9WxFQbxFzbkNcgTwbJZ1So5I8RTkMikU5fSA4Hui8+Tl9Q+ADlLXUWwI/ygsHxX3TD7zWW4CDD253vTalGz+h74"
                   "xfA0aYIZt7xoxKb688NhYuD/H3uOqMp9f5ZOeWi7TIa7o+JNLzwfoP1c8vxQVZ3/Fx1SGbKQ6fgVwDNSLnzgqDXgkjzOu2rJi"
                   "/Thy45y++DMPBGVLTgYWcCrnTh5KvZ42FQbE9z/4vdmOQgk80AEQiLe8P3ljEdMzjKPfj4BVi4yFSPTrhdlmXIwtmvss5NIjD"
                   "gEvYZ5vIOh4Wh/SAAfQ3DkY0iBDSFiJ2JZDTOaCHcM2i37fklkDm/GL/c5Oh7Zou9NxZmcnGvrWk1UKVRpxK96x1wsY42R/So"
                   "ZlN1hYHvOEE0cR19fd6rgDs+noYZ2Hf/8nd2CCadb7iCLzHZV1dwS2213BFDZx2lqkIPIDUeYzEVDs69YW3ifYbwS94UPmzGa"
                   "rAuuyFxPdHuLVqYkkqv1JRWuSyOLLBuIhl44we80ORfvWtJ5fghDpq88p9M8mB+MUQ79TR9Tw75uXVn0EZMXYvJ64Hd9PIiw8"
                   "KR6YV4civaYN1q2i3kkH2PY44Jy6uSCImWnNjRiBgRGNkhLwtcb2EAA2aL2VRyolFXEYdAry9hxjRD+v0km8ts+qR0IlBYMRI"
                   "AoJIIPqUwjoofq4446VrGeVY3b1Krlsd6rUBcIT3LdvsSuqXH6HDcBmKH9s5d1jS/Crkc+BSCcAvl56EiEQvIQS2gH+icpWE5"
                   "I+2Rr1CQezmpXaHGd3YX8soZY9nGz/WNeMLpLzMpgzCmk1TSKc7GgCUYYhIBfA9LT+B8teK/jBe+ZItXfNxMzXREvi/yxt1zG"
                   "y1JvLePhocmTm5DRAmSSlC9/4qR7INI/r2nY9c5h7DjL9AajYQE+/eMFt3vpCxnDIYEIm5uCjvPYft7TMnvQM/joy97TxdLhZ"
                   "J078szg9luBl7hclPdiVo6UpunZkgOgGn0lvmYVS6urPVxBJiuVywyKh+gg2oRxesBb8wugonpy3N3GmPhCY0Pw8anq3vNzXU"
                   "muVASESKQc48z2POP2Mj33raRTLhf3sdiJWrE+hhcyTNy3FC9fu5L4CzxXPrpQ+nne400QGwf9ZokpOxcjr2mCSmhG+cPb4GV"
                   "MsfDubN3feyNdSl0QNuEhoE/rpss3BFq4lxYMbyYtiUhwxnADBYNkjo6AxPI5wXW5Y3MP8sESgqxSZLvRRFtoyT04LP9rtPuk"
                   "xRpqWdMem+qa466l91m/a6gdwAPLhMtYlQ8ZxYDTAH1YrYi3dlj6iqQa9l/eupePyX86iG3VOM/nziLucWpEEB/RmGCyz4Pf3"
                   "/HbdSRNFjCMvKDGxuCAEww+x7y134+ZYh+WH3cRbNxyy+XR9Pslg1btthcJKUekDvovmo5Vq9snBLdfbwrKpd8hE/Bt5JXQzV"
                   "mgoo1AD8NMGlJqCulc7sT3kbjN92eUl8YKo94Q9oHiBifhwI10yb8Cag8GHaYdXp4UVRLJ8f7iPcr3DiTLYWzs7ADakvx/n2h"
                   "37tzsywZ7d/fnmvu98PwBH5Ng0XQ4RXh/RRLHLLAXOqg3ma4gKfarSwCxFJ/d8cSUhNFdAnA+PLOiMIcBRIve3g+51EfIJAmX"
                   "YIVKHgsixZsGPTOKipTrTXMECnmjpAXNkDoxqQNpPH0HAv4Ii5Cf67AGyHR/d1dUM3xzSsTiGfzuiHNpA8ovthoxzuTJvnPvW"
                   "/a66MTTlpZXW3II+Z14hSKMzhtfX0nOLEIaA6WafSlVfCg/uA7j66rXR/zr3yOUdii+HqV7je1lys44z+RSSRpyHEtd6E4joi"
                   "FdsAroNH48BmXA0qrU7/1NdnHX7o1SRG4goP1HPi06tiYvfMx2TzND5TytVStt3N7cDidIFannU7SVCxzzxZwoRwh2hIdnw4D"
                   "IbyKSdEnIYauecuh1QC5SsfUEdp/qA+tCdWs7s0SW60whSu/FZEslvpqeps//WB08O+Ln9ctVrJCHRrwD1WEB/q95zuCLQaQS"
                   "k1E3WLdmyKmwSrjgR3TMVjig8LeWB04TCL1F0n1VaFSwfHBcmK2il6C+y+txhxUuCgQkkFBy03hBP6qM07gEcZ4dBJXqm+hPz"
                   "vViNE7pD/BfryxyWiQoARgjHQqZTtn5VOwXsogZL+GCyC1YUbWwfAMi+bpS/vyrz/h5XeF04jq+5dmMd6N/TqSOyYMRnH/Lh6"
                   "T6/bObonyExz/A38lptBLgFqAZLPSwccawMaPFozsgg4VdBBIS3D1PDEi3f4zyMnanQcBAOyb+J/UDv9OpQPAUe0cbyyCYvYs"
                   "m54CZbbMuEnOY2CXIrL5qkK3Yxlt5yOvD7yok8h+v/wEsu76Hr4XO8c+FIQfZDzIPcwdEpxPko/Wm+QgNqpqWEQmM+1kyzK/I"
                   "k5YQTEfk94vt14KLLNo6YemzvEGQWVvTpD6Qe0qI1SAUon2ICqIAqeD=",
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
    async def get_real_ms_token(cls, logger: Union["BaseLogger", "LoggerManager", "Logger"],
                                proxy: str = None, ) -> dict | None:
        if response := await request_post(logger, cls.API, dumps(cls.DATA | {"tspFromClient": int(time() * 1000)}),
                                          headers=cls.HEADERS, proxy=proxy, ):
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
    print("TikTok", await MsTokenTikTok.get_real_ms_token(Logger(), "http://127.0.0.1:10809"))


if __name__ == "__main__":
    run(demo())
