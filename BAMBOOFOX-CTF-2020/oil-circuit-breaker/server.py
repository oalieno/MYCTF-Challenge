#!/usr/bin/env python3
from ocb import OCB
from os import urandom

encrypt_nonces = []
decrypt_nonces = []

def getData(text):
    data = input(f'{text} = ').strip()
    return bytes.fromhex(data)

def sendData(text, data):
    if type(data) is bytes or type(data) is bytearray:
        print(f'{text} = {data.hex()}')
    else:
        print(f'{text} = {data}')

def encrypt(ocb):
    N = getData('nonce')
    M = getData('plain')

    if b'giveme flag.txt' in M:
        print('[hacker detected] forbidden words')
        exit()

    if N in encrypt_nonces:
        print('[hacker detected] nonce repeating')
        exit()
    encrypt_nonces.append(N)

    C, T = ocb.encrypt(N, M)

    sendData('cipher', C)
    sendData('tag', T)

def decrypt(ocb):
    N = getData('nonce')
    C = getData('cipher')
    T = getData('tag')

    if N in decrypt_nonces:
        print('[hacker detected] nonce repeating')
        exit()
    decrypt_nonces.append(N)

    auth, M = ocb.decrypt(N, C, T)
    
    sendData('auth', auth)
    if auth:
        sendData('plain', M)

def execute(ocb):
    N = getData('nonce')
    C = getData('cipher')
    T = getData('tag')
    
    auth, M = ocb.decrypt(N, C, T)
    
    sendData('auth', auth)
    if auth:
        if M == b'giveme flag.txt':
            with open('./flag.txt') as f:
                print(f.read())
        elif M == b'giveme shit.txt':
            print('shit')
        else:
            print('[unknown command]')

def menu():
    print('1) Encrypt')
    print('2) Decrypt')
    print('3) Execute')
    print('4) Exit')

def main():
    key = urandom(16)
    ocb = OCB(key)
    encrypt_token = 2
    decrypt_token = 1
    while True:
        menu()
        option = input('> ')
        if option == '1':
            if encrypt_token > 0:
                encrypt(ocb)
                encrypt_token -= 1
            else:
                print('[not enough token]')
        elif option == '2':
            if decrypt_token > 0:
                decrypt(ocb)
                decrypt_token -= 1
            else:
                print('[not enough token]')
        elif option == '3':
            execute(ocb)
        else:
            return

main()
