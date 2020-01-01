#!/usr/bin/env python3
from Crypto.Cipher import AES
from os import urandom

BLOCKSIZE = 16

class Block:
    def __init__(self, data = b''):
        self.data = data

    @classmethod
    def random(cls, size):
        return cls(urandom(size))

    @classmethod
    def len(cls, n):
        return cls(int(n * 8).to_bytes(BLOCKSIZE, 'big'))

    @classmethod
    def zero(cls, size = BLOCKSIZE):
        return cls(int(0).to_bytes(size, 'big'))

    def double(self):
        assert(len(self.data) == BLOCKSIZE)
        x = int.from_bytes(self.data, 'big')
        n = BLOCKSIZE * 8
        mask = (1 << n) - 1
        if x & (1 << (n - 1)):
            x = ((x << 1) & mask) ^ 0b10000111
        else:
            x = (x << 1) & mask
        return Block(x.to_bytes(BLOCKSIZE, 'big'))

    def hex(self):
        return self.data.hex()

    def size(self):
        return len(self.data)

    def blocksize(self):
        return len(self.data) // BLOCKSIZE + (len(self.data) % BLOCKSIZE > 0)

    def msb(self, n):
        return Block(self.data[:n])

    def __or__(self, other):
        return Block(self.data + other.data)

    def __xor__(self, other):
        assert(len(self.data) == len(other.data))
        return Block(bytes([x ^ y for x, y in zip(self.data, other.data)]))

    def __eq__(self, other):
        return self.data == other.data

    def __getitem__(self, key):
        return Block(self.data[key * BLOCKSIZE : (key + 1) * BLOCKSIZE])

def bytes_block_bytes(func):
    def wrapper(*args):
        args_new = []
        for arg in args:
            if type(arg) is bytes:
                args_new.append(Block(arg))
            else:
                args_new.append(arg)
        
        results = func(*args_new)

        results_new = []
        for result in results:
            if type(result) is Block:
                results_new.append(result.data)
            else:
                results_new.append(result)

        return tuple(results_new)
    return wrapper

class OCB:
    def __init__(self, key):
        self.aes = AES.new(key, AES.MODE_ECB)
    def e(self, x):
        y = Block(self.aes.encrypt(x.data))
        return y
    def d(self, y):
        x = Block(self.aes.decrypt(y.data))
        return x
    @bytes_block_bytes
    def encrypt(self, N, M):
        L = self.e(N)

        C = Block()
        S = Block.zero()
        for i in range(M.blocksize()):
            L = L.double()
            if i == M.blocksize() - 1:
                pad = self.e(Block.len(M[i].size()) ^ L)
                C |= pad.msb(M[i].size()) ^ M[i]
                S ^= pad ^ (C[i] | Block.zero(BLOCKSIZE - M[i].size()))
            else:
                C |= self.e(M[i] ^ L) ^ L
                S ^= M[i]

        L = L.double() ^ L
        T = self.e(S ^ L)

        return C, T

    @bytes_block_bytes
    def decrypt(self, N, C, T):
        L = self.e(N)

        M = Block()
        S = Block.zero()
        for i in range(C.blocksize()):
            L = L.double()
            if i == C.blocksize() - 1:
                pad = self.e(Block.len(C[i].size()) ^ L)
                M |= pad.msb(C[i].size()) ^ C[i]
                S ^= pad ^ (C[i] | Block.zero(BLOCKSIZE - C[i].size()))
            else:
                M |= self.d(C[i] ^ L) ^ L
                S ^= M[i]

        L = L.double() ^ L
        if T == self.e(S ^ L):
            return True, M
        else:
            return False, None
