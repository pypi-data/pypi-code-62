__author__ = 'Milo Utsch'
__version__ = '0.1.3'

import emoji
import pandas as pd

from take_satisfaction.conversion import convert_answer, convert_item, convert_scale


def test_convert_emojis():
    input_string = '😢'
    converted_string = emoji.demojize(input_string)
    
    assert converted_string not in emoji.UNICODE_EMOJI


def test_convert_action_success():
    action = 'Ajudou'
    scale_reference = {"Nao resolveu": 0, "Nao auxiliou": 0, "Resolveu": 1, "ajudou": 1}
    similarity_threshold = 83
    
    converted_string = convert_answer(action, scale_reference, similarity_threshold)
    
    assert converted_string is 1


def test_convert_convert_item_success():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    scale_reference = {"Nao resolveu": 0, "Nao ajudou": 0, "Resolveu": 1, "ajudou": 1}
    similarity_threshold = 83
    mock_column = 'Action'
    
    result = convert_item(mock_df[mock_column].iloc[0], scale_reference, similarity_threshold)
    assert result is 0


def test_convert_scale_success():
    mock_df = pd.DataFrame([{'Action': 'Nao Ajudou', 'qtd': 200},
                            {'Action': 'Ajudou', 'qtd': 160}
                            ])
    scale_reference = {
        "2": {"Nao resolveu": 0, "Nao ajudou": 0, "Ajudou": 1, "Auxiliou": 1},
        "3":
            {"Amei": 3, "Adorei": 3, "Bom": 2, "Okay": 2, "Nao gostei": 1, "Mais ou menos": 1}
    }
    similarity_threshold = 83
    mock_column = 'Action'
    
    result = convert_scale(mock_df, scale_reference, similarity_threshold, mock_column)
    expected_result = pd.DataFrame(
        [{'Action': 0, 'qtd': 200},
         {'Action': 1, 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)
