#!/usr/bin/env python3
from Crypto.Util.number import *

with open('flag', 'rb') as f:
    flag = int.from_bytes(f.read(), 'big')

def genkeys():
    e = 65537
    while True:
        p, q = getPrime(512), getPrime(512)
        n, phi = p * q, (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            d = inverse(e, phi)
            return n, e, d

def menu():
    print('1) Info')
    print('2) Decrypt')
    print('3) Exit')

def main():
    n, e, d = genkeys()

    while True:
        menu()
        option = input('> ')
        if option == '1':
            c = pow(flag, e, n)
            print(f'c = {c}')
            print(f'n = {n}')
        elif option == '2':
            c = int(input('c = '))
            m = pow(c, d, n)
            print(f'm = {m % 3}')
        else:
            return

main()
