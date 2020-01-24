#!/usr/bin/env python3
import socket
from Crypto.Util.number import *

import sys
sys.setrecursionlimit(10000)

class remote:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.buffer = b''
    def recvuntil(self, text):
        text = self._convert_to_bytes(text)
        while text not in self.buffer:
            self.buffer += self.s.recv(1024)
        index = self.buffer.find(text) + len(text)
        result, self.buffer = self.buffer[:index], self.buffer[index:]
        return result
    def recvline(self):
        return self.recvuntil(b'\n')
    def recvlines(self, n):
        lines = []
        for _ in range(n):
            lines.append(self.recvline())
        return lines
    def _convert_to_bytes(self, text):
        if type(text) is not bytes:
            text = str(text)
        if type(text) is str:
            text = text.encode()
        return text
    def send(self, text):
        text = self._convert_to_bytes(text)
        self.s.sendall(text)
    def sendline(self, text):
        text = self._convert_to_bytes(text)
        self.send(text + b'\n')
    def sendafter(self, prefix, text):
        self.recvuntil(prefix)
        self.send(text)
    def sendlineafter(self, prefix, text):
        self.recvuntil(prefix)
        self.sendline(text)

#r = remote('127.0.0.1', 20000)
r = remote('rayfish.zoolab.org', 20001)

r.sendlineafter('> ', '1')
n = int(r.recvline()[4:])
e = int(r.recvline()[4:])

r.sendlineafter('> ', '2')
c1 = bytes.fromhex(r.recvline()[7:].decode())
r.sendlineafter('> ', '2')
c2 = bytes.fromhex(r.recvline()[7:].decode())
r.sendlineafter('> ', '2')
c3 = bytes.fromhex(r.recvline()[7:].decode())

def gcd(a, b):
    return a.monic() if b == 0 else gcd(b, a % b)

P.<x> = PolynomialRing(Zmod(n))

flag = b''

for i in range(0, len(c1), 128):
    a1 = int.from_bytes(c1[i:i+128], 'big')
    a2 = int.from_bytes(c2[i:i+128], 'big')
    a3 = int.from_bytes(c3[i:i+128], 'big')
    f1 = (a1 - x) ^ e + 2020 * (len(c1) // 128) - (a2 - x) ^ e
    f2 = (a2 - x) ^ e + 2020 * (len(c1) // 128) - (a3 - x) ^ e
    m = -gcd(f1, f2).coefficients()[0]
    flag += long_to_bytes(int(m))

print(flag)
