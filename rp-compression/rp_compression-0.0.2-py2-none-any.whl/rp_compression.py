import numpy as np
import random
import math
import torch


__version__ = '0.0.1'


def gen_random_matrix(row_d, col_d, seed=0, s=1):
    np.random.seed(seed)
    scale_val = math.sqrt(s/col_d)
    random_vec = np.zeros(row_d * col_d)

    for i in range(row_d * col_d):
        random_vec[i] = random.choice([- scale_val,  scale_val])
    return np.reshape(random_vec, (row_d, col_d))

    
def encoding(grad, rd_matrix, side='right'):
    # Set Tensor Type
    if torch.cuda.is_available():
        tensor_type = torch.cuda.FloatTensor
    else:
        tensor_type = torch.FloatTensor

    # Compress Gradient with Random Projection
    rd_matrix = torch.from_numpy(rd_matrix)
    rd_matrix = rd_matrix.type(tensor_type)
    
    if side == 'right':        
        encoding_grad = torch.mm(grad, rd_matrix)
    else:
        encoding_grad = torch.mm(rd_matrix, grad)

    # Return Compressed Gradient
    return encoding_grad


def decoding(grad, rd_matrix, side='right'):
    # Set Tensor Type
    if torch.cuda.is_available():
        tensor_type = torch.cuda.FloatTensor
    else:
        tensor_type = torch.FloatTensor

    rd_matrix = torch.from_numpy(rd_matrix)
    rd_matrix = rd_matrix.type(tensor_type)
    rd_matrix_t = rd_matrix.transpose(0, 1)
    
    # Decompress Compressed Gradient with Random Projection
    if side == 'right':
        decoding_grad = torch.mm(grad, rd_matrix_t)
    else:
        decoding_grad = torch.mm(rd_matrix_t, grad.data)

    # Return Decompressed Gradient
    return decoding_grad
