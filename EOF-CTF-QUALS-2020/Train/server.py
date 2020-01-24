#!/usr/bin/env python3
import os
from Crypto.Util.number import *

with open('flag', 'r') as f:
    flag = f.read()

def genkeys():
    e = 3
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return (n, e), (n, d)

class RSA:
    MODE_CBC = 1

    def __init__(self, key, mode):
        self.pub = key[0]
        self.pri = key[1]
        self.mode = mode

    @classmethod
    def new(cls, key, mode):
        return cls(key, mode)

    def encrypt(self, plain):
        if self.mode == self.MODE_CBC:
            n, e = self.pub
            iv = os.urandom(128)
            prev, cipher = bytes_to_long(iv), b''
            for i in range(0, len(plain), 16):
                x = (prev + bytes_to_long(plain[i:i+16])) % n
                prev = pow(x, e, n)
                cipher += long_to_bytes(prev)
            return iv + cipher
        else:
            raise NotImplementedError

    def decrypt(self, cipher):
        if self.mode == self.MODE_CBC:
            n, d = self.pri
            iv, cipher = cipher[:128], cipher[128:]
            prev, plain = bytes_to_long(iv), b''
            for i in range(0, len(cipher), 128):
                x = pow(bytes_to_long(cipher[i:i+128]), d, n)
                plain += long_to_bytes((x - prev) % n)
                prev = bytes_to_long(cipher[i:i+128])
            return plain

def menu():
    print(f'{"Want to buy some train tickets? ":=^20}')
    print('1) your ticket')
    print('2) use ticket')
    print('3) exit')

def show(rsa):
    session = os.urandom(5).hex()
    (n, e), c = rsa.pub, rsa.encrypt(f'date:2019/1/11|session:{session}|secret:{flag}'.encode())
    print(f'n = {n}')
    print(f'e = {e}')
    print(f'ticket = {c.hex()}')

def use(rsa):
    cipher = bytes.fromhex(input('ticket = '))
    try:
        plain = rsa.decrypt(cipher)
        date, session, secret = plain.split(b'|')
        if date.partition(b':')[2] == b'2019/1/11':
            print('Pass')
        else:
            print('Wrong ticket')
    except:
        print('Oops, our train has some technical issue')

def main():
    pub, pri = genkeys()
    rsa = RSA.new((pub, pri), RSA.MODE_CBC)
    while True:
        menu()
        cmd = input('> ')
        if cmd == '1':
            show(rsa)
        elif cmd == '2':
            use(rsa)
        else:
            print('I have spoken')
            return

main()
