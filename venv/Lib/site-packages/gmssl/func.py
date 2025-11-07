from random import choice


xor = lambda a, b:list(map(lambda x, y: x ^ y, a, b))

rotl = lambda x, n:((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

get_uint32_be = lambda key_data:((key_data[0] << 24) | (key_data[1] << 16) | (key_data[2] << 8) | (key_data[3]))

put_uint32_be = lambda n:[((n>>24)&0xff), ((n>>16)&0xff), ((n>>8)&0xff), ((n)&0xff)]

pkcs7_padding = lambda data, block=16: data + [(16 - len(data) % block)for _ in range(16 - len(data) % block)]

zero_padding = lambda data, block=16: data + [0 for _ in range(16 - len(data) % block)]

pkcs7_unpadding = lambda data: data[:-data[-1]]

zero_unpadding = lambda data,i =1:data[:-i] if data[-i] == 0 else i+1

list_to_bytes = lambda data: b''.join([bytes((i,)) for i in data])

bytes_to_list = lambda data: [i for i in data]

random_hex = lambda x: ''.join([choice('0123456789abcdef') for _ in range(x)])
