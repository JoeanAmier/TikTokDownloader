/**
 * tiktok-web-params.js
 *
 * A pure, dependency-free (Node.js only) re-implementation of the web-side
 * request signing parameters used by tiktok.com:
 *
 *   - X-Dynosaur   (request-bound signature)
 *   - X-Gnarly     (SDK-bound signature)
 *   - X-Bogus      (legacy frontier signature)
 *
 * ────────────────────────────────────────────────────────────────────────
 *  源代码 / Source
 * ────────────────────────────────────────────────────────────────────────
 * 仓库    ：https://github.com/xvhuan/tiktok-web-params
 * 作者    ：xvhuan
 * 协议    ：MIT License
 * 原始文件：tiktok-web-params.js
 * ────────────────────────────────────────────────────────────────────────
 *
 * The implementation is the result of independent, authorized black-box
 * analysis of the public web client for educational purposes. It contains
 * NO browser automation, NO environment emulation and NO remote calls:
 * every value is computed locally from plain arithmetic and primitives
 * (FNV-style hashing, byte encoders, a ChaCha-like stream cipher, RC4 and
 * custom base64 alphabets).
 *
 * ─────────────────────────────────────────────────────────────────────────
 *  ⚠  FOR LEARNING / EXCHANGE ONLY — 仅供学习交流
 *  Use exclusively for authorized testing, security research and education.
 *  Do not use it to bypass rate limits, scrape content, or violate the
 *  Terms of Service of any platform. The author is not responsible for any
 *  misuse. 请仅用于授权测试、安全研究与学习交流，勿用于绕过风控或违反任何
 *  平台服务条款的行为；作者不对任何滥用行为负责。
 * ─────────────────────────────────────────────────────────────────────────
 *
 * @license MIT — see https://github.com/xvhuan/tiktok-web-params/blob/main/LICENSE
 */

'use strict';

/* ------------------------------------------------------------------ *
 *  Pure-JS polyfills: Buffer + MD5 (no require(), no Node.js)
 * ------------------------------------------------------------------ */

const _textEncoder = new TextEncoder();
const _textDecoder = new TextDecoder('latin1');

function _bytesToBase64(bytes) {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    let out = '';
    let i = 0;
    for (; i + 2 < bytes.length; i += 3) {
        const b1 = bytes[i], b2 = bytes[i + 1], b3 = bytes[i + 2];
        out += chars[b1 >> 2];
        out += chars[((b1 & 0x03) << 4) | (b2 >> 4)];
        out += chars[((b2 & 0x0F) << 2) | (b3 >> 6)];
        out += chars[b3 & 0x3F];
    }
    if (i < bytes.length) {
        const b1 = bytes[i];
        out += chars[b1 >> 2];
        if (i + 1 < bytes.length) {
            const b2 = bytes[i + 1];
            out += chars[((b1 & 0x03) << 4) | (b2 >> 4)];
            out += chars[(b2 & 0x0F) << 2];
            out += '=';
        } else {
            out += chars[(b1 & 0x03) << 4];
            out += '==';
        }
    }
    return out;
}

class _ByteBuf extends Uint8Array {
    toString(encoding) {
        if (encoding === 'base64') return _bytesToBase64(this);
        if (encoding === 'hex') {
            let s = '';
            for (let i = 0; i < this.length; i++) s += this[i].toString(16).padStart(2, '0');
            return s;
        }
        return _textDecoder.decode(this);
    }
}

const Buffer = {
    from(input, encoding) {
        if (typeof input === 'string') {
            if (encoding === 'hex') {
                const len = input.length >> 1;
                const out = new _ByteBuf(len);
                for (let i = 0; i < len; i++) out[i] = parseInt(input.substr(i * 2, 2), 16);
                return out;
            }
            if (encoding === 'ascii' || encoding === 'latin1' || encoding === 'binary') {
                const out = new _ByteBuf(input.length);
                for (let i = 0; i < input.length; i++) out[i] = input.charCodeAt(i) & 0xFF;
                return out;
            }
            return new _ByteBuf(_textEncoder.encode(input));
        }
        if (Array.isArray(input)) return new _ByteBuf(input);
        if (input instanceof ArrayBuffer) return new _ByteBuf(input);
        if (input instanceof Uint8Array) return new _ByteBuf(input);
        return new _ByteBuf(0);
    },
    alloc(n, fill = 0) {
        const out = new _ByteBuf(n);
        if (fill !== 0) out.fill(fill);
        return out;
    },
    concat(buffers) {
        let total = 0;
        for (const b of buffers) total += b.length;
        const out = new _ByteBuf(total);
        let offset = 0;
        for (const b of buffers) {
            out.set(b, offset);
            offset += b.length;
        }
        return out;
    },
    isBuffer(obj) { return obj instanceof _ByteBuf; },
};

/* MD5 (RFC 1321) */
const _MD5_K = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391,
];
const _MD5_S = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
];

function _md5Transform(state, block) {
    let a = state[0], b = state[1], c = state[2], d = state[3];
    for (let i = 0; i < 64; i++) {
        let f, g;
        if (i < 16) {
            f = (b & c) | (~b & d);
            g = i;
        } else if (i < 32) {
            f = (b & d) | (c & ~d);
            g = (5 * i + 1) % 16;
        } else if (i < 48) {
            f = b ^ c ^ d;
            g = (3 * i + 5) % 16;
        } else {
            f = c ^ (b | ~d);
            g = (7 * i) % 16;
        }
        f = (f + a + _MD5_K[i] + block[g]) >>> 0;
        a = d;
        d = c;
        c = b;
        b = (b + ((f << _MD5_S[i]) | (f >>> (32 - _MD5_S[i])))) >>> 0;
    }
    state[0] = (state[0] + a) >>> 0;
    state[1] = (state[1] + b) >>> 0;
    state[2] = (state[2] + c) >>> 0;
    state[3] = (state[3] + d) >>> 0;
}

function _md5(input) {
    const bytes = typeof input === 'string' ? _textEncoder.encode(input)
                                            : (input instanceof Uint8Array ? input : new Uint8Array(0));
    const origLen = bytes.length;
    const padLen = (((origLen + 8) >>> 6) + 1) << 6;
    const padded = new Uint8Array(padLen);
    padded.set(bytes);
    padded[origLen] = 0x80;
    const bitLen = origLen * 8;
    padded[padLen - 8] = bitLen & 0xFF;
    padded[padLen - 7] = (bitLen >>> 8) & 0xFF;
    padded[padLen - 6] = (bitLen >>> 16) & 0xFF;
    padded[padLen - 5] = (bitLen >>> 24) & 0xFF;
    const state = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476];
    for (let i = 0; i < padLen; i += 64) {
        const block = new Array(16);
        for (let j = 0; j < 16; j++) {
            block[j] = padded[i + j * 4]
                | (padded[i + j * 4 + 1] << 8)
                | (padded[i + j * 4 + 2] << 16)
                | (padded[i + j * 4 + 3] << 24);
        }
        _md5Transform(state, block);
    }
    let hex = '';
    for (let i = 0; i < 4; i++) hex += state[i].toString(16).padStart(8, '0');
    return hex;
}

const crypto = {
    createHash(algo) {
        if (algo !== 'md5') throw new Error('Only md5 is supported in this runtime');
        const chunks = [];
        return {
            update(data) {
                if (typeof data === 'string') chunks.push(_textEncoder.encode(data));
                else if (data instanceof Uint8Array) chunks.push(data);
                return this;
            },
            digest(encoding) {
                let total = 0;
                for (const c of chunks) total += c.length;
                const combined = new Uint8Array(total);
                let off = 0;
                for (const c of chunks) {
                    combined.set(c, off);
                    off += c.length;
                }
                const hex = _md5(combined);
                if (encoding === 'hex') return hex;
                const out = new _ByteBuf(16);
                for (let i = 0; i < 16; i++) out[i] = parseInt(hex.substr(i * 2, 2), 16);
                return out;
            },
        };
    },
};

/* ------------------------------------------------------------------ *
 *  Internal helpers
 * ------------------------------------------------------------------ */

const _U32 = (x) => x >>> 0;
const _rotl32 = (x, s) => _U32((x << s) | (x >>> (32 - s)));

/** md5 digest (hex) of a Buffer/string. */
function _md5Hex(input) {
    return crypto.createHash('md5').update(input).digest('hex');
}

/**
 * FNV-style state hash (byte-oriented, 32-bit).
 * Verified vectors:
 *   hash('')              = 0x811c9dc4
 *   hash('aid=1988&...')  = URL-query dependent
 */
function hashUrlState(str) {
    let h = _U32(2166136260);
    const bytes = Buffer.from(String(str), 'utf8');
    for (const b of bytes) {
        const h1 = _U32(Math.imul(h ^ b, 16777619));
        h = _U32(h1 + Math.imul(h1, 32));
    }
    return h;
}

/** One of the two string→byte encoders used by the SDK (variant A). */
function _encodeCore(str, cfg) {
    const len = str.length;
    const n = Math.max(len + 2, 6);
    const out = new Uint8Array(n);
    for (let i = 0; i < len; i++) {
        const c = str.charCodeAt(i);
        let v = _U32(c ^ (cfg.xorBase + i));
        v = _U32(v + cfg.addBase + (170 & i)) % 256;
        if (cfg.preXor !== undefined) v = cfg.preXor ^ v;
        v = _U32((v << cfg.rot) | (v >> (8 - cfg.rot))) & 255;
        v = (v ^ 187) + cfg.postAdd;
        out[i] = v % 256;
    }
    for (let i = len; i < n - 2; i++) out[i] = (221 + i) & 255;
    out[n - 2] = 0;
    out[n - 1] = len;
    return out;
}

/** Byte encoder variant A (31434): constants {103, +1, rot2, +1}. */
const encodeBytesA = (s) => _encodeCore(s, {xorBase: 103, addBase: 1, rot: 2, postAdd: 1});

/** Byte encoder variant B (57471): constants {102, +0, preXor165, rot1, +0}. */
const encodeBytesB = (s) => _encodeCore(s, {xorBase: 102, addBase: 0, preXor: 165, rot: 1, postAdd: 0});

/**
 * 32-bit mixer used to derive a request-bound value from
 * (timestamp, random, environment code). Verified vector:
 *   mix(1786633115, 1880707380, 129) === 8491211
 */
function mix(a, b, envcode) {
    let t = _U32((a >> 16) & 0xffff) ^ _U32((b >> 16) & 0xffff);
    t ^= _U32((a & 0xffff) ^ (b & 0xffff));
    return _U32(t | (envcode << 16));
}

/** RC4 (KSA + PRGA). `keyStr` is a 1-byte key in the SDK flow. */
function rc4(keyStr, bytes) {
    const S = Array.from({length: 256}, (_, i) => i);
    let j = 0;
    for (let i = 0; i < 256; i++) {
        j = (j + S[i] + keyStr.charCodeAt(i % keyStr.length)) % 256;
        [S[i], S[j]] = [S[j], S[i]];
    }
    let i = 0;
    j = 0;
    const out = new Uint8Array(bytes.length);
    for (let k = 0; k < bytes.length; k++) {
        i = (i + 1) % 256;
        j = (j + S[i]) % 256;
        [S[i], S[j]] = [S[j], S[i]];
        out[k] = bytes[k] ^ S[(S[i] + S[j]) % 256];
    }
    return out;
}

/* ------------------------------------------------------------------ *
 *  ChaCha-like stream cipher (the encryption core of X-Dynosaur/X-Gnarly)
 * ------------------------------------------------------------------ */

/** One ChaCha quarter-round over lanes a,b,c,d. */
function _qr(t, a, b, c, d) {
    t[a] = _U32(t[a] + t[b]);
    t[d] ^= t[a];
    t[d] = _rotl32(t[d], 16);
    t[c] = _U32(t[c] + t[d]);
    t[b] ^= t[c];
    t[b] = _rotl32(t[b], 12);
    t[a] = _U32(t[a] + t[b]);
    t[d] ^= t[a];
    t[d] = _rotl32(t[d], 8);
    t[c] = _U32(t[c] + t[d]);
    t[b] ^= t[c];
    t[b] = _rotl32(t[b], 7);
}

/** ChaCha block function (state = 16 words, `rounds` iterations), exact SDK layout. */
function chachaBlock(state, rounds) {
    const t = state.slice();
    for (let i = 0; i < rounds && (_qr(t, 0, 4, 8, 12), _qr(t, 1, 5, 9, 13), _qr(t, 2, 6, 10, 14), _qr(
        t, 3, 7, 11, 15), !(++i >= rounds)); ++i
    ) {
        _qr(t, 0, 5, 10, 15);
        _qr(t, 1, 6, 11, 12);
        _qr(t, 2, 7, 12, 13);
        _qr(t, 3, 4, 13, 14);
    }
    for (let o = 0; o < 16; ++o) t[o] = _U32(t[o] + state[o]);
    return t;
}

/** Increment the 32-bit counter at state[12]. */
function incCounter(state) { state[12] = _U32(state[12] + 1); }

/**
 * Stream-encrypt a byte buffer with a 16-word state.
 * `state` = [4 constants] + [12 key words]; counter = state[12].
 */
function encryptPayload(key12, rounds, payload) {
    const state = [1196819126, 600974999, 3863347763, 1451689750].concat(key12.map(_U32));
    const n = payload.length;
    const wlen = Math.ceil(n / 4);
    const words = new Array(wlen);
    for (let f = 0; f < wlen; f++) {
        let w = 0;
        for (let v = 0; v < 4 && 4 * f + v < n; v++) w |= payload[4 * f + v] << (8 * v);
        words[f] = _U32(w);
    }
    const st = state.slice();
    let e;
    for (e = 0; e + 16 < wlen; e += 16) {
        const ks = chachaBlock(st, rounds);
        incCounter(st);
        for (let c = 0; c < 16; c++) words[e + c] ^= ks[c];
    }
    {
        const rem = wlen - e;
        const ks = chachaBlock(st, rounds);
        for (let v = 0; v < rem; v++) words[e + v] ^= ks[v];
    }
    const out = new Uint8Array(n);
    for (let f = 0; f < wlen; f++) {
        for (let v = 0; v < 4 && 4 * f + v < n; v++) out[4 * f + v] = (words[f] >>> (8 * v)) & 255;
    }
    return out;
}

/* ------------------------------------------------------------------ *
 *  Key configuration & final encoding
 * ------------------------------------------------------------------ */

/**
 * Generate the per-request encryption config:
 *   key       — 12 random 32-bit words
 *   rounds    — 5 + Σ(key[i] & 0x0F) mod 16
 *   keyString — the 12 words serialized little-endian (48 bytes)
 */
function makeConfig(randFloat) {
    const key = [];
    const ks = [];
    let acc = 0;
    for (let i = 0; i < 12; i++) {
        const w = _U32(Math.floor(randFloat() * 4294967296));
        key.push(w);
        acc = (acc + (w & 0xf)) & 0xf;
        ks.push(w & 0xff, (w >>> 8) & 0xff, (w >>> 16) & 0xff, (w >>> 24) & 0xff);
    }
    return {key, rounds: acc + 5, keyString: String.fromCharCode(...ks)};
}

/**
 * Splice the 48-byte keyString into the encrypted payload at position
 * `acc = (Σ keyString bytes + Σ cipher bytes) mod (cipherLen + 1)`.
 */
function spliceKeyString(encBytes, keyString) {
    let acc = 0;
    const L1 = encBytes.length + 1;
    for (let i = 0; i < keyString.length; i++) acc = (acc + keyString.charCodeAt(i)) % L1;
    for (let i = 0; i < encBytes.length; i++) acc = (acc + encBytes[i]) % L1;
    const head = Buffer.from(encBytes).subarray(0, acc);
    const tail = Buffer.from(encBytes).subarray(acc);
    return Buffer.concat([head, Buffer.from(keyString, 'latin1'), tail]);
}

/** Custom base64 encoder with a supplied 64-char alphabet (+ '=' padding). */
function customBase64(bytes, alphabet) {
    const std = Buffer.from(bytes).toString('base64');
    const stdA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    let out = '';
    for (const ch of std) out += ch === '=' ? '=' : alphabet[stdA.indexOf(ch)];
    return out;
}

const DYNOSAUR_ALPHABET = 'u09tbS3UvgDEe6r-ZVMXzLpsAohTn7mdINQlW412GqBjfYiyk8JORCF5/xKHwacP';
const BOGUS_ALPHABET = 'Dkdpgh4ZKsQB80/Mfvw36XI1R25+WUAlEi7NLboqYTOPuzmFjJnryx9HVGcaStCe';

/* ------------------------------------------------------------------ *
 *  XOR checksum (SDK op 274)
 * ------------------------------------------------------------------ */

/**
 * XOR checksum over an array.
 *  - mode 1: strings fold to 0
 *  - mode 2: strings fold to their UTF-8 first-4-bytes (big-endian)
 */
function checksumXor(arr, mode) {
    let o = _U32(arr[0]);
    for (let e = 1; e < arr.length; e++) {
        const u = arr[e];
        if (mode === 1 || typeof u === 'number') {
            o ^= _U32(u);
            continue;
        }
        const c = Buffer.from(String(u), 'utf8');
        let f = 0;
        for (let a = 0; a < 4; a++) if (a < c.length) f = (f << 8) | c[a];
        o ^= _U32(f);
    }
    return _U32(o);
}

/* ------------------------------------------------------------------ *
 *  Payload builders
 * ------------------------------------------------------------------ */

const _be16 = (v) => Buffer.from([(v >>> 8) & 255, v & 255]);
const _be32 = (v) => Buffer.from([(v >>> 24) & 255, (v >>> 16) & 255, (v >>> 8) & 255, v & 255]);
const _raw4 = (v) => _be32(_U32(v));
const _md5hex = (s) => _md5Hex(String(s), 'utf8');

/** Default environment (headless/CI-safe values; all fields are customizable). */
const DEFAULT_ENV = Object.freeze({
                                      envcode: 129,   // environment trust code (0x80 = headless/untrusted, 0x01 = base)
                                      ubcode: 14,     // user-behavior code  (2 no-move | 4 no-click | 8 no-keyboard)
                                      txr: 3,         // canvas text render ratio
                                      tfr: 0,         // canvas text fill ratio
                                      ixr: 0,         // canvas image render ratio
                                      ifr: 0,         // canvas image fill ratio
                                  });

/** Build the 25-item TLV payload of X-Dynosaur (keys 0x20..0x38). */
function buildDynosaurPayload({ts, randB, query, ua, env = {}}) {
    const e = {...DEFAULT_ENV, ...env};
    const envcode = e.envcode, ubcode = e.ubcode;
    const mixv = mix(ts, randB, envcode);
    const fields = [
        encodeBytesA('0'),                       // 0x20 placeholder (replaced by checksum)
        encodeBytesB('1'),                       // 0x21
        encodeBytesB('1'),                       // 0x22
        encodeBytesA('0'),                       // 0x23
        encodeBytesA(String(mixv)),              // 0x24 mix(ts, randB, envcode)
        encodeBytesA(String(e.ixr + e.ifr + 1)), // 0x25 canvas image ratio
        encodeBytesA(String(envcode)),           // 0x26 environment code
        encodeBytesA(String(ts)),                // 0x27 timestamp (s)
        encodeBytesA('0'),                       // 0x28
        encodeBytesA('0'),                       // 0x29
        encodeBytesA('5.3.1'),                   // 0x2a scm sub-version
        _raw4(hashUrlState('')),                 // 0x2b hash("")
        encodeBytesA('0'),                       // 0x2c
        encodeBytesA('0'),                       // 0x2d
        _raw4(hashUrlState(query)),              // 0x2e request-query binding
        encodeBytesA(String(e.txr + e.tfr + 1)), // 0x2f canvas text ratio
        _raw4(hashUrlState(ua)),                 // 0x30 user-agent binding
        encodeBytesA('2.0.0.514'),               // 0x31 sdk version
        encodeBytesA('0'),                       // 0x32
        encodeBytesA('0'),                       // 0x33
        encodeBytesA(String(randB)),             // 0x34 random (mix b)
        encodeBytesA('0'),                       // 0x35
        encodeBytesA(String(ubcode)),            // 0x36 user-behavior code
        encodeBytesA('0'),                       // 0x37
        _raw4(hashUrlState('')),                 // 0x38 hash("")
    ];
    // Checksum = XOR of the second byte of every encoded field (placeholder first).
    const cs = checksumXor(fields.map((f) => f[1]), 1);
    fields[0] = encodeBytesB(String(cs));
    const parts = [];
    for (let i = 0; i < fields.length; i++) {
        const field = fields[i];
        parts.push(Buffer.from([0x20 + i, 0, field.length]), field);
    }
    return Buffer.concat(parts);
}

/** Build the 17-item TLV payload of X-Gnarly (leading 0x11 + 17 entries). */
function buildGnarlyPayload({ts, randB, rand2, ua, signedQuery, env = {}}) {
    const e = {...DEFAULT_ENV, ...env};
    const envcode = e.envcode;
    const mixv = mix(ts, randB, envcode);
    const base = [
        0,
        envcode, 14,
        _md5hex(signedQuery), _md5hex(''), _md5hex(ua),
        ts, 0, randB,
        '5.3.1', '2.0.0.514',
        1, 4, 1,
        mixv, rand2,
    ];
    const ret1 = checksumXor(base, 2);
    const ret2 = checksumXor(base.concat([ret1]), 1);
    const fields = {
        0x00: _be32(ret2),
        0x01: _be16(envcode),
        0x02: _be16(14),
        0x03: Buffer.from(_md5hex(signedQuery), 'ascii'),
        0x04: Buffer.from(_md5hex(''), 'ascii'),
        0x05: Buffer.from(_md5hex(ua), 'ascii'),
        0x06: _be32(ts),
        0x07: _be16(0),
        0x08: _be32(randB),
        0x09: Buffer.from('5.3.1'),
        0x0a: Buffer.from('2.0.0.514'),
        0x0b: _be16(1),
        0x0c: _be16(4),
        0x0d: _be16(1),
        0x0e: _be32(mixv),
        0x0f: _be32(rand2),
        0x10: _be32(ret1),
    };
    const parts = [Buffer.from([0x11])];
    for (const k of Object.keys(fields).map(Number).sort((a, b) => a - b)) {
        const f = fields[k];
        parts.push(Buffer.from([k, 0, f.length]), f);
    }
    return Buffer.concat(parts);
}

/** Final signature envelope: header(0x4B) + encrypted+spliced payload → base64. */
function formatSignature(payload, randFloat) {
    const cfg = makeConfig(randFloat);
    const enc = encryptPayload(cfg.key, cfg.rounds, payload);
    const spliced = spliceKeyString(enc, cfg.keyString);
    return customBase64(Buffer.concat([Buffer.from([0x4b]), spliced]), DYNOSAUR_ALPHABET);
}

/* ------------------------------------------------------------------ *
 *  X-Bogus (frontier sign)
 * ------------------------------------------------------------------ */

/**
 * Legacy X-Bogus signature. 16 chars.
 *   data = [index, 0, envcode, ubcode, md5(fp)[14:16], md5(zeros)[14:16], rand]
 *   checksum = XOR(data); prefix = 0x60 | (rand%100 & 0x10); key = rand
 *   X-Bogus = customBase64([prefix, key, ...RC4(chr(key), data+checksum)])
 */
function xBogus({envFp, envcode, ubcode, index, rand}) {
    const fpTail = crypto.createHash('md5').update(Buffer.from(envFp)).digest().subarray(14, 16);
    const zeroTail = crypto.createHash('md5').update(Buffer.alloc(16)).digest().subarray(14, 16);
    const r1 = rand(), r2 = rand(), r3 = rand();
    const data = [
        index & 0xff,
        0,
        envcode & 0xff,
        ubcode & 0xff,
        fpTail[0], fpTail[1],
        zeroTail[0], zeroTail[1],
        Math.floor(r1 * 255),
    ];
    let cs = 0;
    for (const b of data) cs ^= b;
    const prefix = 0x60 | (Math.floor(r2 * 100) & 0x10);
    const key = Math.floor(r3 * 255);
    const enc = rc4(String.fromCharCode(key), Buffer.from([...data, cs]));
    return customBase64(Buffer.from([prefix, key, ...enc]), BOGUS_ALPHABET);
}

/* ------------------------------------------------------------------ *
 *  Public API
 * ------------------------------------------------------------------ */

/**
 * Sign a TikTok web API query string and return all three parameters.
 *
 * @param {string} query   The URL query string, e.g. "aid=1988&count=2".
 * @param {object} [opts]
 * @param {string} [opts.ua]               User-Agent (defaults to a Chrome UA).
 * @param {string} [opts.msToken]          Optional msToken appended to X-Gnarly input.
 * @param {number} [opts.ts]               Unix seconds (defaults to now).
 * @param {number} [opts.randB]            Deterministic random (mix b) for testing.
 * @param {number} [opts.rand2]            Deterministic random for X-Gnarly.
 * @param {number} [opts.bogusIndex]       X-Bogus request counter.
 * @param {object} [opts.env]
 * @param {number} [opts.env.envcode]      Environment trust code (default 129).
 * @param {number} [opts.env.ubcode]       User-behavior code (default 14).
 * @param {number} [opts.env.txr]          Canvas text render ratio.
 * @param {number} [opts.env.tfr]          Canvas text fill ratio.
 * @param {number} [opts.env.ixr]          Canvas image render ratio.
 * @param {number} [opts.env.ifr]          Canvas image fill ratio.
 * @param {Buffer|number[]} [opts.env.fp]  16-byte environment fingerprint.
 * @returns {{ dynosaur: string, gnarly: string, xbogus: string,
 *             dynPayload: Buffer, gnaPayload: Buffer, ts: number,
 *             randB: number, rand2: number }}
 */
function signUrl(query, opts = {}) {
    if (typeof query !== 'string' || query.length === 0) {
        throw new TypeError('query must be a non-empty string');
    }
    const env = opts.env || {};
    const ua = opts.ua || 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36';
    const ts = opts.ts || Math.floor(Date.now() / 1000);
    const randB = _U32(opts.randB ?? Math.floor(Math.random() * 4294967296));
    const rand2 = _U32(opts.rand2 ?? Math.floor(Math.random() * 4294967296));

    const dynPayload = buildDynosaurPayload({ts, randB, query, ua, env});
    const dynosaur = formatSignature(dynPayload, Math.random);

    const signedQuery = query + '&X-Dynosaur=' + dynosaur + '&msToken=' + (opts.msToken || '');
    const gnaPayload = buildGnarlyPayload({ts, randB, rand2, ua, signedQuery, env});
    const gnarly = formatSignature(gnaPayload, Math.random);

    const xbogus = xBogus({
                              envFp: env.fp || Buffer.from('d41d1c8cd9df0b024e9380009f15e2fc', 'hex'),
                              envcode: env.envcode !== undefined ? env.envcode : DEFAULT_ENV.envcode,
                              ubcode: env.ubcode !== undefined ? env.ubcode : DEFAULT_ENV.ubcode,
                              index: opts.bogusIndex || 0,
                              rand: Math.random,
                          });

    return {dynosaur, gnarly, xbogus, dynPayload, gnaPayload, ts, randB, rand2};
}

/* ------------------------------------------------------------------ *
 *  CLI
 * ------------------------------------------------------------------ */

if (typeof require !== 'undefined' && require.main === module) {
    const args = (typeof process !== 'undefined' ? process.argv : []).slice(2);
    if (args.includes('--selftest') || args.includes('--self-test')) {
        // Regression vectors captured from the reference SDK.
        const assert = (typeof require !== 'undefined') ? require('assert') : null;
        assert.strictEqual(hashUrlState(''), 0x811c9dc4);
        assert.strictEqual(hashUrlState('aid=1988&count=2'), 0x6a882875);
        assert.strictEqual(mix(1786633115, 1880707380, 129), 8491211);
        assert.strictEqual(Buffer.from(encodeBytesA('129')).toString('hex'), 'e7d7f7e00003');
        assert.strictEqual(Buffer.from(encodeBytesA('0')).toString('hex'), 'dbdedfe00001');
        assert.strictEqual(Buffer.from(encodeBytesB('54')).toString('hex'), '5656dfe00002');
        const r = signUrl('aid=1988&count=2', {
            ts: 1786638737, randB: 1061263228, rand2: 1061250079,
            ua: 'Mozilla/5.0 (linux) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/24.1.3',
        });
        assert.strictEqual(r.dynosaur.length, 384);
        assert.strictEqual(r.gnarly.length, 332);
        assert.strictEqual(r.xbogus.length, 16);
        assert.strictEqual(r.dynPayload.length, 238);
        assert.strictEqual(r.gnaPayload.length, 198);
        console.log('[selftest] all checks passed');
        if (typeof process !== 'undefined') process.exit(0);
    }
    const query = args[0];
    if (!query) {
        console.error('usage: node tiktok-web-params.js "<query>" [--selftest]');
        if (typeof process !== 'undefined') process.exit(1);
    }
    const out = signUrl(query);
    console.log('X-Dynosaur=' + out.dynosaur);
    console.log('X-Gnarly=' + out.gnarly);
    console.log('X-Bogus=' + out.xbogus);
}

if (typeof module !== 'undefined' && typeof module.exports !== 'undefined') {
    module.exports = {
        signUrl,
        xBogus,
        hashUrlState,
        encodeBytesA,
        encodeBytesB,
        mix,
        rc4,
        chachaBlock,
        encryptPayload,
        buildDynosaurPayload,
        buildGnarlyPayload,
        DEFAULT_ENV,
    };
}
