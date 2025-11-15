from hashlib import md5
from random import randint
from time import time

from src.custom import USERAGENT


class XGnarly:
    _AA = [
        0xFFFFFFFF,
        138,
        1498001188,
        211147047,
        253,
        None,
        203,
        288,
        9,
        1196819126,
        3212677781,
        135,
        263,
        193,
        58,
        18,
        244,
        2931180889,
        240,
        173,
        268,
        2157053261,
        261,
        175,
        14,
        5,
        171,
        270,
        156,
        258,
        13,
        15,
        3732962506,
        185,
        169,
        2,
        6,
        132,
        162,
        200,
        3,
        160,
        217618912,
        62,
        2517678443,
        44,
        164,
        4,
        96,
        183,
        2903579748,
        3863347763,
        119,
        181,
        10,
        190,
        8,
        2654435769,
        259,
        104,
        230,
        128,
        2633865432,
        225,
        1,
        257,
        143,
        179,
        16,
        600974999,
        185100057,
        32,
        188,
        53,
        2718276124,
        177,
        196,
        4294967296,
        147,
        117,
        17,
        49,
        7,
        28,
        12,
        266,
        216,
        11,
        0,
        45,
        166,
        247,
        1451689750,
    ]
    _OT = [_AA[9], _AA[69], _AA[51], _AA[92]]
    _MASK32 = 0xFFFFFFFF
    _BASE64_ALPHABET = (
        "u09tbS3UvgDEe6r-ZVMXzLpsAohTn7mdINQlW412GqBjfYiyk8JORCF5/xKHwacP="
    )

    def __init__(self):
        """
        初始化 XGnarly 实例，并创建其唯一的 PRNG 状态。
        """
        self.St = None
        self._init_prng_state()

    def _init_prng_state(self):
        """
        设置 PRNG 的初始状态，此状态将在此实例的生命周期内持续存在。
        """
        now_ms = int(time() * 1000)
        self.kt = [
            self._AA[44],
            self._AA[74],
            self._AA[10],
            self._AA[62],
            self._AA[42],
            self._AA[17],
            self._AA[2],
            self._AA[21],
            self._AA[3],
            self._AA[70],
            self._AA[50],
            self._AA[32],
            self._AA[0] & now_ms,
            randint(0, self._AA[77]),
            randint(0, self._AA[77]),
            randint(0, self._AA[77]),
        ]
        self.St = self._AA[88]  # position pointer, starts at 0

    # ── BIT HELPERS ────────────────────────────────────────
    @classmethod
    def _u32(cls, x: int) -> int:
        return x & cls._MASK32

    @classmethod
    def _rotl(cls, x: int, n: int) -> int:
        return cls._u32(((x << n) & cls._MASK32) | (x >> (32 - n)))

    # ── CHACHA CORE ────────────────────────────────────────
    @classmethod
    def _quarter(cls, st: list[int], a: int, b: int, c: int, d: int):
        st[a] = cls._u32(st[a] + st[b])
        st[d] = cls._rotl(st[d] ^ st[a], 16)
        st[c] = cls._u32(st[c] + st[d])
        st[b] = cls._rotl(st[b] ^ st[c], 12)
        st[a] = cls._u32(st[a] + st[b])
        st[d] = cls._rotl(st[d] ^ st[a], 8)
        st[c] = cls._u32(st[c] + st[d])
        st[b] = cls._rotl(st[b] ^ st[c], 7)

    @classmethod
    def _chacha_block(cls, state: list[int], rounds: int) -> list[int]:
        w = state.copy()
        r = 0
        while r < rounds:
            cls._quarter(w, 0, 4, 8, 12)
            cls._quarter(w, 1, 5, 9, 13)
            cls._quarter(w, 2, 6, 10, 14)
            cls._quarter(w, 3, 7, 11, 15)
            r += 1
            if r >= rounds:
                break
            cls._quarter(w, 0, 5, 10, 15)
            cls._quarter(w, 1, 6, 11, 12)
            cls._quarter(w, 2, 7, 12, 13)
            cls._quarter(w, 3, 4, 13, 14)
            r += 1
        for i in range(16):
            w[i] = cls._u32(w[i] + state[i])
        return w

    def _bump_counter(self):
        self.kt[12] = self._u32(self.kt[12] + 1)

    # ── JS-faithful PRNG (rand) ────────────────────────────
    def rand(self) -> float:
        e = self._chacha_block(self.kt, 8)
        t = e[self.St]
        r = (e[self.St + 8] & 0xFFFFFFF0) >> 11
        if self.St == 7:
            self._bump_counter()
            self.St = 0
        else:
            self.St += 1
        return (t + 4294967296 * r) / (2**53)

    # ── UTILITIES ──────────────────────────────────────────
    @staticmethod
    def _num_to_bytes(val: int) -> list[int]:
        if val < 65535:
            return [(val >> 8) & 0xFF, val & 0xFF]
        return [(val >> 24) & 0xFF, (val >> 16) & 0xFF, (val >> 8) & 0xFF, val & 0xFF]

    @staticmethod
    def _be_int_from_str(s: str) -> int:
        b = s.encode("utf-8")[:4]
        acc = 0
        for x in b:
            acc = (acc << 8) | x
        return acc & XGnarly._MASK32

    # ── MESSAGE ENCRYPTION ──────────────────────────────
    def _encrypt_chacha(self, key_words: list[int], rounds: int, data: list[int]):
        n_full = len(data) // 4
        leftover = len(data) % 4
        words = [0] * ((len(data) + 3) // 4)

        for i in range(n_full):
            j = 4 * i
            words[i] = (
                data[j] | (data[j + 1] << 8) | (data[j + 2] << 16) | (data[j + 3] << 24)
            )
        if leftover:
            v = 0
            base = 4 * n_full
            for c in range(leftover):
                v |= data[base + c] << (8 * c)
            words[n_full] = v

        o = 0
        state = key_words.copy()
        while o + 16 < len(words):
            stream = self._chacha_block(state, rounds)
            state[12] = self._u32(state[12] + 1)
            for k in range(16):
                words[o + k] ^= stream[k]
            o += 16

        if o < len(words):
            stream = self._chacha_block(state, rounds)
            for k in range(len(words) - o):
                words[o + k] ^= stream[k]

        for i in range(n_full):
            w = words[i]
            j = 4 * i
            data[j : j + 4] = [
                w & 0xFF,
                (w >> 8) & 0xFF,
                (w >> 16) & 0xFF,
                (w >> 24) & 0xFF,
            ]
        if leftover:
            w = words[n_full]
            base = 4 * n_full
            for c in range(leftover):
                data[base + c] = (w >> (8 * c)) & 0xFF

    def _ab22(self, key12_words: list[int], rounds: int, s: str) -> str:
        state = self._OT + key12_words
        data = [ord(ch) for ch in s]
        self._encrypt_chacha(state, rounds, data)
        return "".join(chr(x) for x in data)

    # ── MAIN API ───────────────────────────────────────────
    def generate(
        self,
        query_string: str,
        body: str = "",
        user_agent: str = USERAGENT,
        envcode: int = 0,
        version: str = "5.1.1",
    ) -> str:
        timestamp_ms = int(time() * 1000)

        obj = {
            1: 1,
            2: envcode,
            3: md5(query_string.encode()).hexdigest(),
            4: md5(body.encode()).hexdigest(),
            5: md5(user_agent.encode()).hexdigest(),
            6: timestamp_ms // 1000,
            7: 1508145731,
            8: int((timestamp_ms * 1000) % 2147483648),
            9: version,
        }

        if version == "5.1.1":
            obj[10] = "1.0.0.314"
            obj[11] = 1
            v12 = 0
            for i in range(1, 12):
                v = obj[i]
                to_xor = v if isinstance(v, int) else self._be_int_from_str(v)
                v12 ^= to_xor
            obj[12] = v12 & self._MASK32
        elif version != "5.1.0":
            raise ValueError(f"Unsupported version: {version}")

        v0 = 0
        for i in range(1, len(obj) + 1):
            v = obj[i]
            if isinstance(v, int):
                v0 ^= v
        obj[0] = v0 & self._MASK32

        payload = [len(obj)]
        for k, v in obj.items():
            payload.append(k)
            val_bytes = (
                self._num_to_bytes(v) if isinstance(v, int) else list(v.encode("utf-8"))
            )
            payload.extend(self._num_to_bytes(len(val_bytes)))
            payload.extend(val_bytes)
        base_str = "".join(chr(x) for x in payload)

        key_words = []
        key_bytes = []
        round_accum = 0
        for _ in range(12):
            word = int(self.rand() * 4294967296) & self._MASK32
            key_words.append(word)
            round_accum = (round_accum + (word & 15)) & 15
            key_bytes.extend(
                [
                    word & 0xFF,
                    (word >> 8) & 0xFF,
                    (word >> 16) & 0xFF,
                    (word >> 24) & 0xFF,
                ]
            )
        rounds = round_accum + 5

        enc = self._ab22(key_words, rounds, base_str)

        insert_pos = 0
        for b in key_bytes:
            insert_pos = (insert_pos + b) % (len(enc) + 1)
        for ch in enc:
            insert_pos = (insert_pos + ord(ch)) % (len(enc) + 1)

        key_bytes_str = "".join(chr(b) for b in key_bytes)
        final_str = (
            chr(((1 << 6) ^ (1 << 3) ^ 3) & 0xFF)
            + enc[:insert_pos]
            + key_bytes_str
            + enc[insert_pos:]
        )

        out = []
        full_len = (len(final_str) // 3) * 3
        for i in range(0, full_len, 3):
            block = (
                (ord(final_str[i]) << 16)
                | (ord(final_str[i + 1]) << 8)
                | ord(final_str[i + 2])
            )
            out.extend(
                [
                    self._BASE64_ALPHABET[(block >> 18) & 63],
                    self._BASE64_ALPHABET[(block >> 12) & 63],
                    self._BASE64_ALPHABET[(block >> 6) & 63],
                    self._BASE64_ALPHABET[block & 63],
                ]
            )

        return "".join(out)
