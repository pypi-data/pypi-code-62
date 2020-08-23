from typing import Callable, Optional
import numpy as np

from quple.data_encoding.general_pauli_z_encoding import GeneralPauliZEncoding

class FirstOrderPauliZEncoding(GeneralPauliZEncoding):
    """The first order Pauli Z encoding circuit
    
    An encoding circuit consisting of layers of unitary operators of the
    form exp(iψ(x)Z)H^{⊗n} where ψ is a data encoding function, Z is the 
    Pauli Z operator and x is the data to be encoded.
    
    To encode data of feature dimension n, a set of general Pauli operators 
    are chosen to encode the data into an n qubit circuit. Each Pauli operator
    will contribute to a unitary operation \exp(i\sum_{s\in S}ψ_s(x_s)Z_s)H^{⊗n}
    where S is the set of qubit indices for all qubits in the circuit.
    
    """
    def __init__(self, feature_dimension: int,
                 copies:int=2, 
                 encoding_map:Optional[Callable[[np.ndarray], float]] = None,
                 name:str='FirstOrderPauliZEncoding', *args, **kwargs):
        '''Creates first order Pauli Z encoding circuit
        
        Examples:
        >> cq = FirstOrderPauliZEncoding(feature_dimension=4, copies=2)
        >> cq
        (0, 0): ───H───Rz(pi*x_0)───H───Rz(pi*x_0)───

        (0, 1): ───H───Rz(pi*x_1)───H───Rz(pi*x_1)───

        (0, 2): ───H───Rz(pi*x_2)───H───Rz(pi*x_2)───

        (0, 3): ───H───Rz(pi*x_3)───H───Rz(pi*x_3)───
        
        Args:
            feature_dimension: int
                Dimension of data to be encoded (=number of qubits in the circuit)
            copies: int
                Number of repetition of the encoding circuit
            encoding_map: function that maps a numpy array to a number
                Data mapping function from R^(feature_dimension) to R
            name: str
                Name of the encoding circuit
        '''        
        super().__init__(feature_dimension, copies=copies, z_order=1,
                         encoding_map=encoding_map, name=name,
                         *args, **kwargs)