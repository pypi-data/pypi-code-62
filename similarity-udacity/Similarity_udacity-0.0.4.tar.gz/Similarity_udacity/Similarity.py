import numpy as np
from scipy.stats import rankdata

def mean(X):

  '''Calculates the mean of a series of data
        Accepts:
        list of tupples
        list of lists
        numpy array
  '''

  #Sanity Check
  assert len(X) != 0,'empty object'

  X = np.array(X)
  mean = sum(X)/len(X)
  return mean


def median(X):

  '''Calculate the median a series of data
      Accepts:
        list of tupples
        list of lists
        numpy array
  '''

  #Sanity Checks
  assert len(X) != 0,'empty object'

  X = sorted(X)
  X = np.array(X)
  lenght = len(X)

  if lenght % 2 == 0:
    p = int(lenght / 2)
    median = (X[p-1] + X[p]) / 2
    return median

  else:
    p = int((lenght)/2)
    return X[p]



def var(X):
  '''Calculates the varivance of a series of data
      Accepts:
        list of tupples
        list of lists
        numpy array
  '''

  #Sanity Checks
  assert len(X) != 0,'empty object'

  X = np.array(X)
  _mean = mean(X)

  diff = X - _mean
  var = sum(diff*diff)/len(X)
  return var


def correlation(X,Y):
  """Calculates Pearson's Correlation Coeficient a series of data
      Accepts:
        list of tupples
        list of lists
        numpy array
  """
  #Sanity Checks
  assert len(X) != 0,'empty object X'
  assert len(Y) != 0,'empty object Y'
  assert len(X) == len(Y),'unequal nummber of elements'

  lenght = len(X)
  

  _mean_y =mean(Y)
  _mean_x = mean(X)

  _mean_diff_y = Y - _mean_y
  _mean_diff_x = X - _mean_x

  numerator = sum(_mean_diff_y * _mean_diff_x )/ lenght
  denominator = np.sqrt(var(X))*np.sqrt(var(Y))

  return round(numerator / denominator ,4)



def euclidean_distance(X,Y):
  '''Calculates euclidean distance a series of data
      Accepts:
        list of tupples
        list of lists
        numpy array
        '''

  X = np.array(X)
  Y = np.array(Y)
  
  #Sanity Checks
  assert X.shape[0] != 0,'empty object X'
  assert Y.shape[0] != 0,'empty object Y'
  assert X.shape == Y.shape,'unequal nummber of elements'


  _euclid_dis = np.round(np.sqrt(np.sum(np.square(X-Y),axis = 1)), decimals=4)

  return _euclid_dis



def manhatten_distance(X,Y):
  '''Calculates manhatten distance a series of data
      Accepts:
        list of tupples
        list of lists
        numpy array
        '''

  X = np.array(X)
  Y = np.array(Y)
  
  #Sanity Checks
  assert X.shape[0] != 0,'empty object X'
  assert Y.shape[0] != 0,'empty object Y'
  assert X.shape == Y.shape,'unequal nummber of elements'


  manhatten_dis = np.round(np.sum(np.absolute(X-Y),axis = 1), decimals=4)
  return manhatten_dis


def spearman_rho(X,Y):

  X = np.array(X)
  Y = np.array(Y)

  X,Y = rankdata(X),rankdata(Y)

  _mean_y,_mean_x  = mean(Y), mean(X)
  _mean_diff_y,_mean_diff_x = Y - _mean_y, X - _mean_x
  

  _numerator = np.sum(_mean_diff_y * _mean_diff_x)
  _denominator = np.sqrt(np.sum(_mean_diff_y **2 ))*np.sqrt(np.sum(_mean_diff_x**2))

  rho = round(_numerator/_denominator,3)
  return rho

