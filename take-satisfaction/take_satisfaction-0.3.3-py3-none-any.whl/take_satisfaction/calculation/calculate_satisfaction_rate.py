__author__ = 'Milo Utsch'
__version__ = '0.1.1'

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
    mean = weighted_mean(df[level_column], df[quantities_column])
    return scale(mean, min(df[level_column]), max(df[level_column]))
