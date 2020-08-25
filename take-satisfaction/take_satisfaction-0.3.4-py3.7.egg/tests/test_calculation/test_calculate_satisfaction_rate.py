__author__ = 'Milo Utsch'
__version__ = '0.1.0'

import pandas as pd

from take_satisfaction.calculation import calculate_satisfaction_rate


def test_calculate_satisfaction_rate():
    mock_data = [{'Action': 1, 'qtd': 119964},
                 {'Action': 0, 'qtd': 92767}
                 ]
    mock_df = pd.DataFrame(mock_data)
    mock_level_column = 'Action'
    mock_quantities_column = 'qtd'
    
    satisfaction_rate = calculate_satisfaction_rate(mock_df, mock_level_column, mock_quantities_column)
    
    assert isinstance(satisfaction_rate, float)
    assert satisfaction_rate == 0.563923452623266
