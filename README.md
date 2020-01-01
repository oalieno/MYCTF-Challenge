# MY CTF Challenge

## BAMBOOFOX CTF 2018

### baby-lea

| category | solves |
| :-: | :-: |
| CRYPTO | 11 / 150 |

Classic **length extension attack**

Just use [hashpump](https://github.com/bwall/HashPump)

### baby-lea-revenge

| category | solves |
| :-: | :-: |
| CRYPTO | 3 / 150 |

Inspired by **HITCON CTF 2017 - secret server**

Base on the `baby-lea` challenge

This time `token` is encrypted with AES

But notice what the `unpad` function do is just removing the bytes according to the last byte without checking

So we could append any number of blocks to the token and use `unpad` function to remove it completely without affecting the auth code

Meantime, the token in `if b"user=admin" in token` is the token before `unpad`

Here is the question, how do we modify the plain text without knowing the key of AES?

If we already know a pair of (IV, ciphertext, plaintext), we could modify the plaintext to anothertext by adjusting the IV to `IV ^ plaintext ^ anothertext`

It's CBC magic

### baby-lea-impossible

| category | solves |
| :-: | :-: |
| CRYPTO | 2 / 150 |

Inspired by **HITCON CTF 2017 - secret server**

Base on the `baby-lea-revenge` challenge

This time we need to make the token after `unpad` exactly the same as "user=admin"

Also, the original token is forbidden, that is we can't use it to alter the token

But notice that salt is also affected by `unpad`, together with token

So we can leak salt by controlling the last byte and make the plaintext be `salt[:1], salt[:2], salt[:3], ...`

Then try sending auth code with value `sha256('a'), sha256('b'), sha256('c'), ...` to bruteforce each character

Here is the question, how do we modify the plain text without using the original token

Just leak whatever plaintext you want with the previous trick :)

### mini-padding

| category | solves |
| :-: | :-: |
| CRYPTO | 6 / 150 |

Classic **padding oracle attack**

Just write a script

### toddler-notakto

| category | solves |
| :-: | :-: |
| PWN | 1 / 150 |

This challenge has one-null-byte-overflow, overflow the last byte of `_IO_buf_base` and got a arbitary write

Since the binary is `partial RELRO`, just modify one of the functions at GOT table to one_gadget

### toddler-notakto-revenge

| category | solves |
| :-: | :-: |
| PPC | 12 / 150 |

Use my repo: [Notakto](https://github.com/OAlienO/Notakto)

### toddler-notakto-impossible

| category | solves |
| :-: | :-: |
| PPC | 0 / 150 |

Use my repo: [Notakto](https://github.com/OAlienO/Notakto)

## BAMBOOFOX CTF 2020

### Oracle

| category | points | solves |
| :-: | :-: | :-: |
| CRYPTO | 270 | 28 / 837 |

RSA LSB oracle

### Oil Circuit Breaker

| category | points | solves |
| :-: | :-: | :-: |
| CRYPTO | 714 | 5 / 837 |

The attack follow this paper https://eprint.iacr.org/2019/311.pdf

To do universal forgery with only 2 encryption oracles and 1 decryption oracles.  
First use 1 encryption oracle and 1 decryption oracle to get a few of random mappings.  
Then, you can brute force the last byte of the block to get the ciphertext and tag with only 1 encryption oracle.
