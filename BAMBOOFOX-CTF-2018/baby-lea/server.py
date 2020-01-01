#!/usr/bin/env python3
import hashlib
from base64 import b64encode, b64decode

with open('flag', 'rb') as data:
    flag = data.read()

with open('salt', 'rb') as data:
    salt = data.read()
    assert(len(salt) == 44)

def main():
    try:
        token = b64encode(b"user=someone")
        auth = hashlib.sha256(salt + b64decode(token)).hexdigest()

        print("your token:", token.decode('ascii'))
        print("your authentication code:", auth)

        token = input("input your token: ").strip()
        auth = input("input your authentication code: ").strip()

        if auth == hashlib.sha256(salt + b64decode(token.encode('ascii'))).hexdigest():
            if b"user=admin" in b64decode(token):
                print(flag.decode('utf-8'))
            else:
                print("YOU ARE NOT ADMIN, GO AWAY!")
        else:
            print("YOU ARE NOT ALLOW TO CHANGE MY TOKEN!")
    except:
        exit(0)

if __name__ == '__main__':
    main()
