__author__ = 'Milo Utsch'
__version__ = '0.1.5'

import typing as tp

import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

DF = pd.DataFrame
S = pd.Series


def remove_manual(df: DF, manual_entries: tp.List[str], threshold: int, column: str) -> DF:
    """Checks for a manual entry row in the scale and removes it.
    
    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param manual_entries: Manual entry variations.
    :type manual_entries: ``list`` of ``str``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :param column: Target column to be analysed.
    :type column: ``str``
    :return: Dataframe with the bot scale without manual entries.
    :rtype: ``pandas.DataFrame``
    """
    validate_preprocess_df(df, column)
    return df[~match_manual(df[column], manual_entries, threshold)]


def validate_preprocess_df(df: DF, answer_column: str) -> None:
    """Validates if df is not empty and has answer column.

    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param answer_column: Column containing answers.
    :type answer_column: ``str``
    :return: None.
    """
    assert not df.empty, "Cannot process empty scale"
    assert answer_column in df.columns, f"Scale does not contain answer column {answer_column}"


def match_manual(series: S, reference: tp.List[str], threshold: int) -> np.ndarray:
    """Returns a series describing whether each element in the series is a manual entry.
    
    :param series: Series.
    :type series: ``pandas.Series``
    :param reference: Manual entry variations.
    :type reference: ``list`` of ``str``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :return: Series describing whether each element is a manual entry.
    :rtype: ``numpy.ndarray`` of ``bool``
    """
    return np.array([
        (isinstance(sample, str) and any(fuzz.ratio(sample.lower(), entry.lower()) >= threshold for entry in reference))
        for sample in series
    ])
