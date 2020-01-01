#!/usr/bin/env python3
from oracle import Oracle
from block import *

oracle = Oracle('127.0.0.1', 20000)

def randomMapping(n):
    N = Block.random(16)
    M = Block.random(n * 16) | Block.len(16) | Block.random(16)
    C, T = oracle.encrypt(N, M)

    S = Block.zero()
    C_ = Block()
    T_ = M[n + 1] ^ C[n + 1]
    for i in range(n):
        C_ |= C[i]
        S ^= M[i]
    C_ |= (S ^ C[n] ^ Block.len(16))
    auth, M_ = oracle.decrypt(N, C_, T_)
    assert(auth == 'True')
    
    S = Block.zero()
    for i in range(n):
        S ^= M[i]
    L = (S ^ M_[n] ^ Block.len(16)).half(n + 1) 

    mappings = []
    for i in range(n):
        mappings.append((M[i] ^ L.double(i + 1), C[i] ^ L.double(i + 1)))

    return mappings

def specificMapping(Is):
    global mappingIndex
    N, L = mappingPool[mappingIndex]
    mappingIndex += 1

    n = len(Is)
    M = Block()
    for i in range(n):
        M |= (Is[i] ^ L.double(i + 1))
    M |= Block.zero()
    C, T = oracle.encrypt(N, M)

    Os = []
    for i in range(n):
        Os.append(C[i] ^ L.double(i + 1))

    return Os

def execute(M):
    global mappingIndex
    N, L = mappingPool[mappingIndex]
    mappingIndex += 1

    n = M.blocksize()
    X = []
    S = Block.zero()
    for i in range(n - 1):
        X.append(M[i] ^ L.double(i + 1))
        S ^= M[i]
    X.append(Block.len(M[n - 1].size()) ^ L.double(n))

    SS = []
    for i in range(2 ** 8):
        SS.append(S ^ (M[n - 1] | Block(bytes([i]))) ^ L.double(n + 1) ^ L.double(n))

    Y = specificMapping(X + SS)
    
    C = Block()
    for i in range(n - 1):
        C |= Y[i] ^ L.double(i + 1)
    C |= Y[n - 1].msb(M[n - 1].size()) ^ M[n - 1]
    
    T = Y[n + Y[n - 1].data[-1]]

    auth, flag = oracle.execution(N, C, T)

    print(flag)

mappingPool = randomMapping(10)
mappingIndex = 0
M = Block(b'giveme flag.txt')
execute(M)
