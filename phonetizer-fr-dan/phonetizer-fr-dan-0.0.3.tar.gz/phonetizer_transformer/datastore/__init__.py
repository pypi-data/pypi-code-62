import os

import pandas as pd
from sklearn.model_selection import train_test_split
from torchtext.data import Field, BucketIterator

from ..utils import (
    load_lexique_nn, char_in_col_to_dict, split_char, device
)

from .dataframe_dataset import DataFrameDataset


BATCH_SIZE = 128


def build_iterators():
    lexique = load_lexique_nn()
    all_characters, all_characters_rev = char_in_col_to_dict(lexique, 'ortho')
    all_phonems, all_phonems_rev = char_in_col_to_dict(lexique, 'phon')

    SRC = Field(tokenize = split_char,
                init_token = '<sos>',
                eos_token = '<eos>',
                batch_first = True)

    TRG = Field(tokenize = split_char,
                init_token = '<sos>',
                eos_token = '<eos>',
                batch_first = True)

    X = lexique.ortho
    y = lexique.phon

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.25, random_state=1234)
    train_df = pd.DataFrame({'ortho': X_train, 'phon': y_train})
    val_df = pd.DataFrame({'ortho': X_val, 'phon': y_val})
    test_df = pd.DataFrame({'ortho': X_test, 'phon': y_test})

    train_data, valid_data, test_data = DataFrameDataset.splits(
    ortho_field=SRC, phon_field=TRG,
    train_df=train_df, val_df=val_df, test_df=test_df)

    SRC.build_vocab(train_data, min_freq = 2)
    TRG.build_vocab(train_data, min_freq = 2)

    train_iterator, valid_iterator, test_iterator = BucketIterator.splits(
        (train_data, valid_data, test_data), 
        batch_size = BATCH_SIZE,
        device = device())
    return train_iterator, valid_iterator, test_iterator, SRC, TRG
