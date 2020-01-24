#!/usr/bin/env python3
from pwn import remote
from Crypto.Util.number import *

'''
00 date:2019/1/11|s
16 ession:000000000
32 0|secret:flagfla
48 gflagflagflagfla
'''

r = remote('127.0.0.1', 20000)

r.sendlineafter('> ', '1')
n = int(r.recvline()[4:])
e = int(r.recvline()[4:])
ticket = bytes.fromhex(r.recvline()[9:].decode())
iv, ticket = ticket[:128], ticket[128:]

flag = b''

f = b''
now = list(map(bytes_to_long, [ticket[128:256], ticket[256:384]]))
borrow = 0
for i in range(0, 7):
    for j in range(1, 256):
        now[0] += 1 << (8 * i)
        r.sendlineafter('> ', '2')
        r.sendlineafter('ticket = ', b''.join(map(long_to_bytes, now)).hex())
        if b'Oops' not in r.recvline():
            x = ord('|') + j + borrow
            if x > 255:
                borrow = 1
                x %= 256
            f = bytes([x]) + f
            print(f)
            now[0] += 1 << (8 * i)
            break

flag += f

f = b''
now = list(map(bytes_to_long, [ticket[256:384], ticket[384:512]]))
now[0] -= ord('|') << (8 * 20)
borrow = 0
for i in range(0, 16):
    for j in range(1, 256):
        now[0] += 1 << (8 * i)
        r.sendlineafter('> ', '2')
        r.sendlineafter('ticket = ', b''.join(map(long_to_bytes, now)).hex())
        if b'Oops' not in r.recvline():
            x = ord('|') + j + borrow
            if x > 255:
                borrow = 1
                x %= 256
            f = bytes([x]) + f
            print(f)
            now[0] += 1 << (8 * i)
            break

flag += f

print(flag)
