from functools import reduce
import os
import pandas as pd
import torch
import torch.nn as nn


MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(MODULE_DIR, '..', 'data/')


def load_lexique():
    data_files = [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))]
    if 'lexique.parquet' in data_files:
        df = pd.read_parquet(os.path.join(DATA_PATH, 'lexique.parquet'))
    else:
        df = pd.read_csv('http://www.lexique.org/databases/Lexique383/Lexique383.tsv', sep='\t')
        df = df[['ortho', 'phon', 'orthosyll', 'syll']]
        df.to_parquet(os.path.join(DATA_PATH, 'lexique.parquet'))
    return df


def load_lexique_nn():
    data_files = [f for f in os.listdir(DATA_PATH) if os.path.isfile(os.path.join(DATA_PATH, f))]
    if 'lexique_nn.parquet' in data_files:
        df = pd.read_parquet(os.path.join(DATA_PATH, 'lexique_nn.parquet'))
    else:
        df = load_lexique()
        df = (
            df
            .loc[lambda row: (~ row.orthosyll.isna())]
            .loc[lambda row: (~ row.syll.isna())]
            .loc[lambda row: (~ row.ortho.isna())]
            .loc[lambda row: (~ row.ortho.str.contains(r"-| |'").astype(bool))]
            .loc[lambda row: row.syll.str.count('-') == row.orthosyll.str.count('-')]
        )
        df = df[['ortho', 'phon']]
        df.to_parquet(os.path.join(DATA_PATH, 'lexique_nn.parquet'))
    return df


def char_in_col_to_dict(df, col):
    """
    Get all caracters in col and map them to dict.
    Example:
    ```
    maison
    avion
    ````
    becomes {0: 'a', 1: 'i', 2: 'm', 3: 'n', 4: 'o', 5: 's', 6: 'v' }
    """
    assert col in df.columns
    all_chars = reduce(lambda a,b : str(a)+str(b), df[col].values)
    dict_char = dict(enumerate(list(set(all_chars))))
    reverse_dict = {value: key for key, value in dict_char.items()}
    return dict_char, reverse_dict


def split_char(text):
    return [char for char in text]

def device():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def initialize_weights(m):
    if hasattr(m, 'weight') and m.weight.dim() > 1:
        nn.init.xavier_uniform_(m.weight.data)

def epoch_time(start_time, end_time):
    elapsed_time = end_time - start_time
    elapsed_mins = int(elapsed_time / 60)
    elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
    return elapsed_mins, elapsed_secs
