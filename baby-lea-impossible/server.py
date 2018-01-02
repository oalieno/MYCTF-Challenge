#!/usr/bin/env python3
import os
import string
import random
import hashlib
import binascii
from base64 import b64encode, b64decode
from Crypto.Cipher import AES

with open('flag', 'rb') as data:
    flag = data.read()

with open('salt', 'rb') as data:
    salt = data.read()

with open('key', 'rb') as data:
    key = data.read()

def pad(text):
    padding = 16 - len(text) % 16
    return text + bytes([padding] * padding)

def unpad(text):
    padding = text[-1]
    return text[:-padding]

def encrypt(iv, text):
    aes = AES.new(key, AES.MODE_CBC, iv)
    text = aes.encrypt(text)
    return text

def decrypt(iv, text):
    aes = AES.new(key, AES.MODE_CBC, iv)
    text = aes.decrypt(text)
    return text

def out_message(iv, text):
    text = encrypt(iv, text)
    message = b64encode(iv + text)
    return message

def in_message(message, forbid):
    iv, text = b64decode(message)[:16], b64decode(message)[16:]
    if forbid in text:
        print("HACKER DETECTED")
        exit(0)
    text = decrypt(iv, text)
    return text

def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)]).encode('ascii')
    digest = hashlib.sha256(proof).hexdigest()
    print("SHA256(XXXX + {}) == {}".format(proof[4:].decode('ascii'), digest))
    x = input('Give me XXXX:').strip()
    if len(x) != 4 or hashlib.sha256(x.encode('ascii') + proof[4:]).hexdigest() != digest:
        exit(0)

def main():
    proof_of_work()

    IV = os.urandom(16)
    token = b"user=someone"
    auth = hashlib.sha256(salt + token).hexdigest()
    token = out_message(IV, pad(token))
    forbid = b64decode(token)[16:]

    print("your token:", token.decode('ascii'))
    print("your authentication code:", auth)

    while True:
        try:
            token = input("input your token: ").strip()
            auth = input("input your authentication code: ").strip()

            token = in_message(token, forbid)
            token = unpad(salt + token)

            if auth == hashlib.sha256(token).hexdigest():
                if token == salt + b"user=admin":
                    print(flag.decode('utf-8'))
                else:
                    print("YOU ARE NOT ADMIN, GO AWAY!")
            else:
                print("YOU ARE NOT ALLOW TO CHANGE MY TOKEN!")
        except:
            exit(0)

if __name__ == '__main__':
    main()
