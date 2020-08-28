import numpy as np

def generate_random_sequences(N,T):
    sequences = np.zeros((N,T),np.int32)
    for i in range(N):
        sequence = np.random.choice([0,1], T)
        sequences[i] = sequence
    return sequences

def generate_sequence(T,M,V,A,B,pi):
    s = np.random.choice(range(M), p=pi) # initial state
    x = np.random.choice(range(V), p = B[s]) # initial observation
    sequence = [x]
    for n in range(T-1):
        s = np.random.choice(range(M), p=A[s]) # next state
        x = np.random.choice(range(V), p=B[s]) # cd ..next observation
        sequence.append(x)
    return sequence

def generate_sequences(N,T,M,V,A,B,pi):
    sequences = np.zeros((N,T),np.int32)
    for i in range(N):
        sequences[i] = generate_sequence(T,M,V,A,B,pi)
    return sequences
