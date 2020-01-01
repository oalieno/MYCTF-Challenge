#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import *

r = remote('127.0.0.1', 20000)

r.sendlineafter('> ', '1')
c = int(r.recvline()[4:])
n = int(r.recvline()[4:])
e = 65537

def oracle(x):
    r.sendlineafter('> ', '2')
    r.sendlineafter('c = ', str(x))
    m = int(r.recvline()[4:])
    return m

L, H, R = 0, 1, 1

s = 1
while True:
    s = s * pow(3, e, n) % n 
    m = oracle(s * c % n)
    
    L, H, R = 3 * L, 3 * H, 3 * R
    
    if m == 0:
        H -= 2
    elif m == (-n % 3):
        L += 1
        H -= 1
    else:
        L += 2

    if (n * H // R) - (n * L // R) < 2:
        break

print(long_to_bytes(n * L // R))
print(long_to_bytes(n * H // R))

r.interactive()
