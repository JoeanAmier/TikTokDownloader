from typing import Union, Dict, Iterable, Optional

Buffer = bytes|bytearray|memoryview

from Cryptodome.Cipher._mode_ecb import EcbMode
from Cryptodome.Cipher._mode_cbc import CbcMode
from Cryptodome.Cipher._mode_cfb import CfbMode
from Cryptodome.Cipher._mode_ofb import OfbMode
from Cryptodome.Cipher._mode_ctr import CtrMode
from Cryptodome.Cipher._mode_openpgp import OpenPgpMode
from Cryptodome.Cipher._mode_eax import EaxMode

DESMode = int

MODE_ECB: DESMode
MODE_CBC: DESMode
MODE_CFB: DESMode
MODE_OFB: DESMode
MODE_CTR: DESMode
MODE_OPENPGP: DESMode
MODE_EAX: DESMode

def new(key: Buffer,
        mode: DESMode,
        iv : Optional[Buffer] = ...,
        IV : Optional[Buffer] = ...,
        nonce : Optional[Buffer] = ...,
        segment_size : int = ...,
        mac_len : int = ...,
        initial_value : Union[int, Buffer] = ...,
        counter : Dict = ...) -> \
        Union[EcbMode, CbcMode, CfbMode, OfbMode, CtrMode, OpenPgpMode]: ...

block_size: int
key_size: int
