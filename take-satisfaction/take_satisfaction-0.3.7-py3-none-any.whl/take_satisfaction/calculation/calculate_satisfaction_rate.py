__author__ = 'Milo Utsch'
__version__ = '0.1.2'

import pandas as pd

from take_satisfaction.utils import weighted_mean
from take_satisfaction.utils import scale

DF = pd.DataFrame
S = pd.Series

    
def calculate_satisfaction_rate(df: DF, level_column: str, quantities_column: str) -> float:
    """ Calculates the satisfaction rate based on the bot scale.

    :param df: Dataframe with satisfaction levels and its quantities.
    :type df: ``pandas.Dataframe``
    :param level_column: Satisfaction level column.
    :type level_column: ``str``
    :param quantities_column: Satisfaction level quantities column.
    :type quantities_column: ``str``
    :return: Satisfaction rate.
    :rtype: ``float``
    """
    validate_satisfaction_data(df, level_column, quantities_column)
    mean = weighted_mean(df[level_column], df[quantities_column])
    return scale(mean, min(df[level_column]), max(df[level_column]))


def validate_satisfaction_data(df, answer_column, quantity_column):
    """Validates if df is not empty, if it has an answer column and a quantity column.

    :param df: Dataframe.
    :type df: ``pandas.DataFrame``
    :param answer_column: Column containing answers.
    :type answer_column: ``str``
    :param quantity_column: Column containing quantities.
    :type quantity_column: ``str``
    :return: None.
    """
    assert not df.empty, "Cannot process empty scale"
    assert answer_column in df.columns, f"Scale does not contain answer column {answer_column}"
    assert quantity_column in df.columns, f"Scale does not contain quantity column {quantity_column}"
