import pandas as pd
import numpy as np


def _iter_randomstate(x):
    # generate 100 random numbers between 1 and 10
    np.random.randint(10, size=100)


def gen_sample_data():
    # create a dataframe from which we'll draw a random sample from
    df = pd.DataFrame({"reproducible": ["NO"]*1000})
    df.iloc[565] = "YES"
    return df

def try_reproducible_split(df):
    # seed the random number generator
    np.random.seed(0)

    # iterate numpy's random state
    # groupby operates a bit differently between different versions of pandas,
    # so iterating the random state through a groupby should yield 
    # unreproducible results
    df.groupby('reproducible').apply(_iter_randomstate)

    # select a random sample; the random sample chosen should be different 
    # depending on the version of pandas used
    result = df.sample(1)

    return result.values[0][0]

if __name__ == '__main__':
    df = gen_sample_data()
    is_reproducible = try_reproducible_split(df)
    print("the random sample is reproducible:", is_reproducible)