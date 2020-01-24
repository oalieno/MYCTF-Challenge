#!/usr/bin/env python3
import socket
from Crypto.Util.number import *

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

r = remote('rayfish.zoolab.org', 20000)

r.sendlineafter('> ', '1')
n = int(r.recvline()[4:])
e = int(r.recvline()[4:])

r.sendlineafter('> ', '3')
r.sendlineafter('plain = ', '00')
nonce = bytes.fromhex(r.recvline()[9:].decode())

nonce = (int.from_bytes(nonce, 'big') ^ 3) % n

r.sendlineafter('> ', '2')
c = bytes.fromhex(r.recvline()[7:].decode())

P.<x> = PolynomialRing(Zmod(n))

flag = b''

for i in range(0, len(c), 128):
    nonce = (nonce + 2020) % n
    a = int.from_bytes(c[i:i+128], 'big')
    f = (a - x) ^ 3 - nonce
    flag += long_to_bytes(int(f.monic().small_roots()[0]))

print(flag)
