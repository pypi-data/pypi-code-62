from .Similarity import *
from scipy.stats import spearmanr
import numpy as np

x = [9, 10, 12, 13, 13, 13, 15, 15, 16, 16, 18, 22, 23, 24, 24,25]
y = [7, 12, 10, 13, 13, 15, 20, 5, 3, 5, 32, 22, 17, 13, 11, 19]
A,B = [(1,2),(2,2),(3,5)],[(9,8),(5,6),(1,2)]

def test_mean():
    assert mean(x) == 16.75,'Error with mean function' 

def test_median():
    assert median(x) == 15.5,'Error with median function' 

def test_var(): 
    assert var(x) == 26.1875,'Error with var function'

def test_corr():
    assert correlation(x,y) == 0.3519,'Error with corr function' 

def test_spearman():
    assert spearman_rho(x,y) == round(spearmanr(x,y)[0],3),'Error with spearman function' 

def test_manhatten():
    assert (manhatten_distance(A,B) == np.array([14,7,5])).all(),'Error with manhatten distance function'
    
def test_euclidean():
    assert (euclidean_distance(A,B) == np.array([10,5,3.6056])).all(),'Error with euclidean distancefunction' 
