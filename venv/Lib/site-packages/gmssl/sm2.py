import binascii
from random import choice
from . import sm3, func
from Cryptodome.Util.asn1 import DerSequence, DerInteger
from binascii import unhexlify
# 选择素域，设置椭圆曲线参数

default_ecc_table = {
    'n': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123',
    'p': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF',
    'g': '32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7'
         'bc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0',
    'a': 'FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC',
    'b': '28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93',
}


class CryptSM2(object):

    def __init__(self, private_key, public_key, ecc_table=default_ecc_table, mode=0, asn1=False):
        """
        mode: 0-C1C2C3, 1-C1C3C2 (default is 1)
        """
        self.private_key = private_key
        self.public_key = public_key.lstrip("04") if public_key.startswith("04") else public_key
        self.para_len = len(ecc_table['n'])
        self.ecc_a3 = (
            int(ecc_table['a'], base=16) + 3) % int(ecc_table['p'], base=16)
        self.ecc_table = ecc_table
        assert mode in (0, 1), 'mode must be one of (0, 1)'
        self.mode = mode
        self.asn1 = asn1

    def _kg(self, k, Point):  # kP运算
        Point = '%s%s' % (Point, '1')
        mask_str = '8'
        for i in range(self.para_len - 1):
            mask_str += '0'
        mask = int(mask_str, 16)
        Temp = Point
        flag = False
        for n in range(self.para_len * 4):
            if (flag):
                Temp = self._double_point(Temp)
            if (k & mask) != 0:
                if (flag):
                    Temp = self._add_point(Temp, Point)
                else:
                    flag = True
                    Temp = Point
            k = k << 1
        return self._convert_jacb_to_nor(Temp)

    def _double_point(self, Point):  # 倍点
        l = len(Point)
        len_2 = 2 * self.para_len
        if l < self.para_len * 2:
            return None
        else:
            x1 = int(Point[0:self.para_len], 16)
            y1 = int(Point[self.para_len:len_2], 16)
            if l == len_2:
                z1 = 1
            else:
                z1 = int(Point[len_2:], 16)

            T6 = (z1 * z1) % int(self.ecc_table['p'], base=16)
            T2 = (y1 * y1) % int(self.ecc_table['p'], base=16)
            T3 = (x1 + T6) % int(self.ecc_table['p'], base=16)
            T4 = (x1 - T6) % int(self.ecc_table['p'], base=16)
            T1 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (y1 * z1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * 8) % int(self.ecc_table['p'], base=16)
            T5 = (x1 * T4) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * 3) % int(self.ecc_table['p'], base=16)
            T6 = (T6 * T6) % int(self.ecc_table['p'], base=16)
            T6 = (self.ecc_a3 * T6) % int(self.ecc_table['p'], base=16)
            T1 = (T1 + T6) % int(self.ecc_table['p'], base=16)
            z3 = (T3 + T3) % int(self.ecc_table['p'], base=16)
            T3 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            x3 = (T3 - T5) % int(self.ecc_table['p'], base=16)

            if (T5 % 2) == 1:
                T4 = (T5 + ((T5 + int(self.ecc_table['p'], base=16)) >> 1) - T3) % int(
                    self.ecc_table['p'], base=16)
            else:
                T4 = (T5 + (T5 >> 1) - T3) % int(self.ecc_table['p'], base=16)

            T1 = (T1 * T4) % int(self.ecc_table['p'], base=16)
            y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)

            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (x3, y3, z3)

    def _add_point(self, P1, P2):  # 点加函数，P2点为仿射坐标即z=1，P1为Jacobian加重射影坐标
        len_2 = 2 * self.para_len
        l1 = len(P1)
        l2 = len(P2)
        if (l1 < len_2) or (l2 < len_2):
            return None
        else:
            X1 = int(P1[0:self.para_len], 16)
            Y1 = int(P1[self.para_len:len_2], 16)
            if (l1 == len_2):
                Z1 = 1
            else:
                Z1 = int(P1[len_2:], 16)
            x2 = int(P2[0:self.para_len], 16)
            y2 = int(P2[self.para_len:len_2], 16)

            T1 = (Z1 * Z1) % int(self.ecc_table['p'], base=16)
            T2 = (y2 * Z1) % int(self.ecc_table['p'], base=16)
            T3 = (x2 * T1) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T3 - X1) % int(self.ecc_table['p'], base=16)
            T3 = (T3 + X1) % int(self.ecc_table['p'], base=16)
            T4 = (T2 * T2) % int(self.ecc_table['p'], base=16)
            T1 = (T1 - Y1) % int(self.ecc_table['p'], base=16)
            Z3 = (Z1 * T2) % int(self.ecc_table['p'], base=16)
            T2 = (T2 * T4) % int(self.ecc_table['p'], base=16)
            T3 = (T3 * T4) % int(self.ecc_table['p'], base=16)
            T5 = (T1 * T1) % int(self.ecc_table['p'], base=16)
            T4 = (X1 * T4) % int(self.ecc_table['p'], base=16)
            X3 = (T5 - T3) % int(self.ecc_table['p'], base=16)
            T2 = (Y1 * T2) % int(self.ecc_table['p'], base=16)
            T3 = (T4 - X3) % int(self.ecc_table['p'], base=16)
            T1 = (T1 * T3) % int(self.ecc_table['p'], base=16)
            Y3 = (T1 - T2) % int(self.ecc_table['p'], base=16)

            form = '%%0%dx' % self.para_len
            form = form * 3
            return form % (X3, Y3, Z3)

    def _convert_jacb_to_nor(self, Point):  # Jacobian加重射影坐标转换成仿射坐标
        len_2 = 2 * self.para_len
        x = int(Point[0:self.para_len], 16)
        y = int(Point[self.para_len:len_2], 16)
        z = int(Point[len_2:], 16)
        z_inv = pow(
            z, int(self.ecc_table['p'], base=16) - 2, int(self.ecc_table['p'], base=16))
        z_invSquar = (z_inv * z_inv) % int(self.ecc_table['p'], base=16)
        z_invQube = (z_invSquar * z_inv) % int(self.ecc_table['p'], base=16)
        x_new = (x * z_invSquar) % int(self.ecc_table['p'], base=16)
        y_new = (y * z_invQube) % int(self.ecc_table['p'], base=16)
        z_new = (z * z_inv) % int(self.ecc_table['p'], base=16)
        if z_new == 1:
            form = '%%0%dx' % self.para_len
            form = form * 2
            return form % (x_new, y_new)
        else:
            return None

    def verify(self, Sign, data):
        # 验签函数，sign签名r||s，E消息hash，public_key公钥
        if self.asn1:
            unhex_sign = unhexlify(Sign.encode())
            seq_der = DerSequence()
            origin_sign = seq_der.decode(unhex_sign)
            r = origin_sign[0]
            s = origin_sign[1]
        else:
            r = int(Sign[0:self.para_len], 16)
            s = int(Sign[self.para_len:2*self.para_len], 16)
        e = int(data.hex(), 16)
        t = (r + s) % int(self.ecc_table['n'], base=16)
        if t == 0:
            return 0

        P1 = self._kg(s, self.ecc_table['g'])
        P2 = self._kg(t, self.public_key)
        # print(P1)
        # print(P2)
        if P1 == P2:
            P1 = '%s%s' % (P1, 1)
            P1 = self._double_point(P1)
        else:
            P1 = '%s%s' % (P1, 1)
            P1 = self._add_point(P1, P2)
            P1 = self._convert_jacb_to_nor(P1)

        x = int(P1[0:self.para_len], 16)
        return r == ((e + x) % int(self.ecc_table['n'], base=16))

    def sign(self, data, K):
        """
        签名函数, data消息的hash，private_key私钥，K随机数，均为16进制字符串
        :param self: 
        :param data: data消息的hash
        :param K: K随机数
        :return: 
        """
        E = data.hex()  # 消息转化为16进制字符串
        e = int(E, 16)

        d = int(self.private_key, 16)
        k = int(K, 16)

        P1 = self._kg(k, self.ecc_table['g'])

        x = int(P1[0:self.para_len], 16)
        R = ((e + x) % int(self.ecc_table['n'], base=16))
        if R == 0 or R + k == int(self.ecc_table['n'], base=16):
            return None
        d_1 = pow(
            d+1, int(self.ecc_table['n'], base=16) - 2, int(self.ecc_table['n'], base=16))
        S = (d_1*(k + R) - R) % int(self.ecc_table['n'], base=16)
        if S == 0:
            return None
        elif self.asn1:
            return DerSequence([DerInteger(R), DerInteger(S)]).encode().hex()
        else:
            return '%064x%064x' % (R, S)

    def encrypt(self, data):
        # 加密函数，data消息(bytes)
        msg = data.hex()  # 消息转化为16进制字符串
        k = func.random_hex(self.para_len)
        C1 = self._kg(int(k, 16), self.ecc_table['g'])
        xy = self._kg(int(k, 16), self.public_key)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:2*self.para_len]
        ml = len(msg)
        t = sm3.sm3_kdf(xy.encode('utf8'), ml/2)
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % ml
            C2 = form % (int(msg, 16) ^ int(t, 16))
            C3 = sm3.sm3_hash([
                i for i in bytes.fromhex('%s%s%s' % (x2, msg, y2))
            ])
            if self.mode:
                return bytes.fromhex('%s%s%s' % (C1, C3, C2))
            else:
                return bytes.fromhex('%s%s%s' % (C1, C2, C3))

    def decrypt(self, data):
        # 解密函数，data密文（bytes）
        data = data.hex()
        len_2 = 2 * self.para_len
        len_3 = len_2 + 64
        C1 = data[0:len_2]

        if self.mode:
            C3 = data[len_2:len_3]
            C2 = data[len_3:]
        else:
            C2 = data[len_2:-64]
            C3 = data[-64:]

        xy = self._kg(int(self.private_key, 16), C1)
        # print('xy = %s' % xy)
        x2 = xy[0:self.para_len]
        y2 = xy[self.para_len:len_2]
        cl = len(C2)
        t = sm3.sm3_kdf(xy.encode('utf8'), cl/2)
        if int(t, 16) == 0:
            return None
        else:
            form = '%%0%dx' % cl
            M = form % (int(C2, 16) ^ int(t, 16))
            u = sm3.sm3_hash([
                i for i in bytes.fromhex('%s%s%s' % (x2, M, y2))
            ])
            return bytes.fromhex(M)

    def _sm3_z(self, data):
        """
        SM3WITHSM2 签名规则:  SM2.sign(SM3(Z+MSG)，PrivateKey)
        其中: z = Hash256(Len(ID) + ID + a + b + xG + yG + xA + yA)
        """
        # sm3withsm2 的 z 值
        z = '0080'+'31323334353637383132333435363738' + \
            self.ecc_table['a'] + self.ecc_table['b'] + self.ecc_table['g'] + \
            self.public_key
        z = binascii.a2b_hex(z)
        Za = sm3.sm3_hash(func.bytes_to_list(z))
        M_ = (Za + data.hex()).encode('utf-8')
        e = sm3.sm3_hash(func.bytes_to_list(binascii.a2b_hex(M_)))
        return e

    def sign_with_sm3(self, data, random_hex_str=None):
        sign_data = binascii.a2b_hex(self._sm3_z(data).encode('utf-8'))
        if random_hex_str is None:
            random_hex_str = func.random_hex(self.para_len)
        sign = self.sign(sign_data, random_hex_str)  # 16进制
        return sign

    def verify_with_sm3(self, sign, data):
        sign_data = binascii.a2b_hex(self._sm3_z(data).encode('utf-8'))
        return self.verify(sign, sign_data)
