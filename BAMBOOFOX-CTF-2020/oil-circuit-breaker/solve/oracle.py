#!/usr/bin/env python3
from pwn import *
from block import Block

class Oracle:
    def __init__(self, ip, port):
        self.r = remote(ip, port)

    def __del__(self): 
        self.r.sendline('4')

    def getData(self, text, hex = True):
        self.r.recvuntil(f'{text} = ')
        if hex:
            data = bytes.fromhex(self.r.recvline().strip().decode())
            print(f'[+] get {text} = {data.hex()}')
        else:
            data = self.r.recvline().strip().decode()
            print(f'[+] get {text} = {data}')
        return data

    def sendData(self, text, data):
        self.r.sendlineafter(f'{text} = ', data.hex())
        print(f'[+] send {text} = {data.hex()}')

    def encrypt(self, N, M):
        print('-' * 10)
        print('Encryption Oracle')
        print('-' * 10)
        self.r.sendlineafter('> ', '1')
        self.sendData('nonce', N)
        self.sendData('plain', M)
        C = Block(self.getData('cipher'))
        T = Block(self.getData('tag'))
        print()
        return C, T

    def decrypt(self, N, C, T):
        print('-' * 10)
        print('Decryption Oracle')
        print('-' * 10)
        self.r.sendlineafter('> ', '2')
        self.sendData('nonce', N)
        self.sendData('cipher', C)
        self.sendData('tag', T)
        auth = self.getData('auth', hex = False)
        M = None
        if auth == 'True':
            M = Block(self.getData('plain'))
        print()
        return auth, M
    
    def execution(self, N, C, T):
        print('-' * 10)
        print('Execution Oracle')
        print('-' * 10)
        self.r.sendlineafter('> ', '3')
        self.sendData('nonce', N)
        self.sendData('cipher', C)
        self.sendData('tag', T)
        auth = self.getData('auth', hex = False)
        M = None
        if auth == 'True':
            M = self.r.recvline()
        print()
        return auth, M
