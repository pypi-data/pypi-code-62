from typing import List, Union, Optional, Callable, Sequence
import numpy as np
from pdb import set_trace

import cirq

from quple.data_encoding import EncodingCircuit
from quple.circuits.templates.pauli_block import PauliBlock

class GeneralPauliEncoding(EncodingCircuit):
    '''The general Pauli encoding circuit
    
    An encoding circuit consisting of layers of unitary operators of the
    form exp(iψ(x)Σ)H^{⊗n} where ψ is a data encoding function, Σ is a
    generalized Pauli operator from the general Pauli group G_n 
    which is an n-fold tensor product of Pauli operators on n
    qubits, and x is the data to be encoded.
    
    To encode data of feature dimension n, a set of general Pauli operators 
    are chosen to encode the data into an n qubit circuit. Each Pauli operator
    will contribute to a unitary operation \exp(i\sum_{s\in S}ψ_s(x_s)Σ_s) where
    s is the indices of a subset of all qubit indices S. For a general Pauli 
    operator of order k, s is a tuple of k elements. 
    
    For example, suppose the Pauli operator Σ = Z is used, then S is the set
    {1, 2, ..., n} and the unitary operation is \exp(i\sum_{j=1}^n ψ_j(x_j)Z_j)H^{⊗n}, 
    where Z_j is the Pauli Z operator acting on the j-th qubit. 
    
    If instead the Pauli Operator Σ = Z⊗Z is used, then S is a set of 2-tuple of
    qubit indices determined by the interaction graph. For a fully connected
    graph, S is the set of combinations of 2-qubit pairs. Then the unitary operation
    is \exp(i\sum{s=(j, k) in S}ψ_{j,k}(x_j, x_k)Z_j⊗Z_k)H^{⊗n}
    '''    
    def __init__(self, feature_dimension: int,
                 copies:int=2, paulis:List[str] = ['Z', 'ZZ'],
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str='GeneralPauliEncoding',*args, **kwargs):
        '''Creates the general Pauli encoding circuit
        
        Examples:
        >> cq = GeneralPauliEncoding(feature_dimension=3, paulis=['XX'], copies=2)
        >> cq
        (0, 0): ───H───H───@──────────────────────@───H───H───@──────────────────────@───H──────────────────────────────────────
                           │                      │           │                      │
        (0, 1): ───H───H───X───Rz(pi*<x_0*x_1>)───X───H───────┼──────────────────────┼───H───────@──────────────────────@───H───
                                                              │                      │           │                      │
        (0, 2): ───H──────────────────────────────────────H───X───Rz(pi*<x_0*x_2>)───X───H───H───X───Rz(pi*<x_1*x_2>)───X───H───
        
        Args:
            feature_dimension: int
                Dimension of data to be encoded (=number of qubits in the circuit)
            copies: int
                Number of repetition of the encoding circuit
            encoding_map: function that maps a numpy array to a number
                Data mapping function from R^(feature_dimension) to R
            paulis: list of str
                Pauli operations to be performed on each entangling block
            name: str
                Name of the encoding circuit
        '''
        GeneralPauliEncoding._validate_paulis(paulis)
        pauli_blocks = [PauliBlock(pauli) for pauli in paulis]
        super().__init__(feature_dimension, copies=copies, 
                         entanglement_blocks=pauli_blocks,
                         encoding_map=encoding_map, name=name,
                        *args, **kwargs)
        self.paulis = paulis
        
    @staticmethod
    def _validate_paulis(paulis:List[str]):
        for pauli_str in paulis:
            for pauli in pauli_str:
                if pauli not in ['Z','X','Y','I']:
                    raise ValueError('Invalid Pauli operation: {}'.format(pauli))