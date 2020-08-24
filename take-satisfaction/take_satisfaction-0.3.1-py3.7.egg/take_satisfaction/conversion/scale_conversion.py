__author__ = 'Milo Utsch and Gabriel Salgado'
__version__ = '0.1.7'
__all__ = [
    'select_reference',
    'convert_answer',
    'convert_item',
    'convert_scale'
]

import typing as tp

import unidecode as uni
import emoji
import pandas as pd
from fuzzywuzzy import fuzz

DF = pd.DataFrame
SR = pd.Series


def select_reference(df: DF, reference: tp.Dict[str, tp.Dict[str, int]]) -> tp.Dict[str, int]:
    """Selects a scale reference based on the number of distinct scale answers.

    Raises an exception if there is not reference for this df.

    :param df: Dataframe with answers.
    :type df: ``pandas.Dataframe``
    :param reference: Dictionary containing answer name variations.
    :type reference: ``dict`` from ``str`` to ``dict`` from ``str`` to ``int``
    :return: Reference for answers on suitable scale for df.
    :rtype: ``dict`` from ``str`` to ``int``
    """
    scale_size = str(len(df))
    
    if str(scale_size) not in reference:
        raise Exception(f'Not found scale for size {scale_size}.')
    
    return reference[scale_size]


def convert_answer(answer: str, reference: tp.Dict[str, int], threshold: int) -> int:
    """Converts answer to its corresponding satisfaction level.

    Answer is like "Gostei", "Muito ruim"...
    And corresponding level range from negative to positive.
    Raises an exception if there is not reference similar enough.

    :param answer: String with scale answer.
    :type answer: ``str``
    :param reference: Dictionary with answer variations.
    :type reference: ``dict`` from ``str`` to ``int``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :return: Corresponding satisfaction level.
    :rtype: ``int``
    """
    similarity = [
        (fuzz.ratio(uni.unidecode(answer.lower()), key), value)
        for key, value in reference.items()
    ]
    max_similarity, level = max(similarity)
    if max_similarity >= threshold:
        return level
    raise Exception(f'Scale not found for {answer}.')


def convert_item(item: tp.Any, reference: tp.Dict[str, int], threshold: int) -> int:
    """Converts item to suitable satisfaction level.

    Raises an exception if the conversion  fails.

    :param item: Scale item.
    :type item: ``Any``
    :param reference: Dictionary with answer variations.
    :type reference: ``dict`` from ``str`` to ``int``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :return: Satisfaction level.
    :rtype: ``int`
    """
    if isinstance(item, str):
        return convert_answer(emoji.demojize(item), reference, threshold)
    return item


def convert_scale(df: DF, references: tp.Dict[str, tp.Dict[str, int]], threshold: int, column: str) -> DF:
    """Converts scale df answers to its suitable satisfaction level.

    Raises an exception if the conversion fails.

    :param df: Dataframe with answers.
    :type df: ``pandas.Dataframe``
    :param references: Mapping scale sizes to suitable reference.
    :type references: ``dict`` from ``str`` to ``dict`` from ``str`` to ``int``
    :param threshold: Minimum similarity for str matching.
    :type threshold: ``int``
    :param column: Column with answers on dataframe.
    :type column: ``str``
    :return: Dataframe with answer column converted to satisfaction level.
    :rtype: ``pandas.Dataframe``
    """
    scale_reference = select_reference(df, references)
    converted_scale = df.copy()
    converted_scale[column] = df[column].apply(convert_item, args=(scale_reference, threshold))
    return converted_scale
