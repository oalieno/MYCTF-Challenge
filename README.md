# MY CTF Challenge

## baby-lea

Solved: **11 / 150**  
Category: **CRYPTO**

Classic **length extension attack**

Just use [hashpump](https://github.com/bwall/HashPump)

## baby-lea-revenge

Solved: **3 / 150**  
Category: **CRYPTO**

Inspired by **HITCON CTF 2017 - secret server**

Base on the `baby-lea` challenge

I encrypt the `token` with AES

But notice the `unpad` function just remove the bytes according to the last byte without checking

So we could append two blocks to the token and use `unpad` to remove it completely without affecting the auth code

And the token in `if b"user=admin" in token` is the token before `unpad`

Here is the question, how do we modify the plain text without knowing the key of AES?

If we already know a pair of (IV, ciphertext, plaintext), we could modify the plaintext to anothertext by adjusting the IV to `IV ^ plaintext ^ anothertext`

It's CBC magic

## baby-lea-impossible

Solved: **2 / 150**  
Category: **CRYPTO**

Inspired by **HITCON CTF 2017 - secret server**

Base on the `baby-lea-revenge` challenge

This time we need to make the token after `unpad` exactly same as "user=admin"

And the original token is forbidden, that is we can't use it to alter the token

But remember that salt is also `unpad`, together with token

So we can leak salt by controlling the last byte and make the plaintext be salt[:1], salt[:2], salt[:3], ...

Then try sending auth code with value `sha256('a')`, `sha256('b')`, `sha256('c')`, ... to bruteforce each characters

Here is the question, how do we modify the plain text without using the original token

Just leak the whatever plaintext you want with the previous trick :)

## mini-padding

Solved: **6 / 150**  
Category: **CRYPTO**

Classic **padding oracle attack**

Just write a script

## toddler-notakto

Solved: **1 / 150**  
Category: **PWN**

This challenge has one-null-byte-overflow, overflow the last byte of `_IO_buf_base` and got a arbitary write

Since the binary is `partial RELRO`, just modify the one of the functions at GOT table to one_gadget

## toddler-notakto-revenge

Solved: **12 / 150**  
Category: **PPC**

Use my repo: [Notakto](https://github.com/OAlienO/Notakto)

## toddler-notakto-impossible

Solved: **0 / 150**  
Category: **PPC**

Use my repo: [Notakto](https://github.com/OAlienO/Notakto)
