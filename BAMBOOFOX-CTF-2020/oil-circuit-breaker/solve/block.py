#!/usr/bin/env python3
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

    def double(self, y = 1):
        assert(len(self.data) == BLOCKSIZE)
        x = int.from_bytes(self.data, 'big')
        n = BLOCKSIZE * 8
        mask = (1 << n) - 1
        for _ in range(y):
            if x & (1 << (n - 1)):
                x = ((x << 1) & mask) ^ 0b10000111
            else:
                x = (x << 1) & mask
        return Block(x.to_bytes(BLOCKSIZE, 'big'))

    def half(self, y = 1):
        assert(len(self.data) == BLOCKSIZE)
        x = int.from_bytes(self.data, 'big')
        n = BLOCKSIZE * 8
        for _ in range(y):
            if x & 1:
                x = ((x ^ 0b10000111) >> 1) | (1 << (n - 1))
            else:
                x = x >> 1
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
