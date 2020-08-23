# -*- coding: utf-8 -*-
import autograd.numpy as np

from wdl.util import memoize, WeightsParser,wdl_lose_fun
from wdl.rdkit_utils import smiles_to_fps,smiles_to_fps1
#from rdkit.Chem import MACCSkeys
#from pychem.pychem import PyChem2d
import rdkit.Chem as Chem


def batch_normalize(activations):
    mbmean = np.mean(activations, axis=0, keepdims=True)
    return (activations - mbmean) / (np.std(activations, axis=0, keepdims=True) + 1)

#def relu(X):
#    out = X * (X > 0)               
#    return out, X
def relu(X):
    return X * (X > 0)

#    "Rectified linear activation function."


def sigmoid(x):
    return 0.5*(np.tanh(x) + 1)
    
def mean_squared_error(predictions, targets):
    return np.mean((predictions - targets)**2, axis=0)

def categorical_nll(predictions, targets):
    return -np.mean(predictions * targets)

def binary_classification_nll(predictions, targets):
    """Predictions is a real number, whose sigmoid is the probability that
     the target is 1."""
    pred_probs = sigmoid(predictions)
    label_probabilities = pred_probs * targets + (1 - pred_probs) * (1 - targets)
    return -np.mean(np.log(label_probabilities))

def build_standard_net(layer_sizes, normalize, L2_reg, L1_reg=0.0, activation_function=relu,
                       nll_func=wdl_lose_fun):
    """Just a plain old neural net, nothing to do with molecules.
    layer sizes includes the input size."""
    layer_sizes = layer_sizes + [1]

    parser = WeightsParser()
    for i, shape in enumerate(zip(layer_sizes[:-1], layer_sizes[1:])):
        parser.add_weights(('weights', i), shape)
        parser.add_weights(('biases', i), (1, shape[1]))

    def predictions(W_vect, X):
        cur_units = X
        for layer in range(len(layer_sizes) - 1):
            cur_W = parser.get(W_vect, ('weights', layer))
            cur_B = parser.get(W_vect, ('biases', layer))
            cur_units = np.dot(cur_units, cur_W) + cur_B
            if layer < len(layer_sizes) - 2:
                if normalize:
                    cur_units = batch_normalize(cur_units)
                cur_units = activation_function(cur_units)
        return cur_units[:, 0]

    def loss(w, X, targets):
        assert len(w) > 0
        log_prior = -L2_reg * np.dot(w, w) /(2*len(w)+0.0000001) - L1_reg * np.mean(np.abs(w))
        preds = predictions(w, X)
        return nll_func(preds, targets) - log_prior

    return loss, predictions, parser


def build_fingerprint_deep_net(net_params, fingerprint_func, fp_parser, fp_l2_penalty):
    """Composes a fingerprint function with signature (smiles, weights, params)
     with a fully-connected neural network."""
    net_loss_fun, net_pred_fun, net_parser = build_standard_net(**net_params)

    combined_parser = WeightsParser()
    combined_parser.add_weights('fingerprint weights', (len(fp_parser),))
    combined_parser.add_weights('net weights', (len(net_parser),))

    def unpack_weights(weights):
        fingerprint_weights = combined_parser.get(weights, 'fingerprint weights')
        net_weights         = combined_parser.get(weights, 'net weights')
        return fingerprint_weights, net_weights

    def loss_fun(weights, smiles, targets):
        fingerprint_weights, net_weights = unpack_weights(weights)
        fingerprints = fingerprint_func(fingerprint_weights, smiles)
        net_loss = net_loss_fun(net_weights, fingerprints, targets)
        if len(fingerprint_weights) > 0 and fp_l2_penalty > 0:
            return net_loss + fp_l2_penalty * np.mean(fingerprint_weights**2)
        else:
            return net_loss

    def pred_fun(weights, smiles):
        fingerprint_weights, net_weights = unpack_weights(weights)
        fingerprints = fingerprint_func(fingerprint_weights, smiles)
        return net_pred_fun(net_weights, fingerprints)

    return loss_fun, pred_fun, combined_parser

