__author__ = 'Milo Utsch'
__version__ = '0.1.1'

import numpy as np
import pandas as pd

from take_satisfaction.preprocess import match_manual
from take_satisfaction.preprocess import remove_manual


def test_get_manual_entries_success_two_items():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160},
         {'Action': 'Entrada Manual', 'qtd': 5}]
    )
    mock_similarity = 85
    mock_manual_ref = ["entrada manual", "entrada digitada", "entrada do usuario", "input manual", "user input",
                       "input_inesperado"]
    mock_column = 'Action'
    
    manual_entries = match_manual(mock_df[mock_column], mock_manual_ref, mock_similarity)
    
    assert isinstance(manual_entries, np.ndarray)
    expected_result = np.array([False, False, True])
    assert all(manual_entries == expected_result)


def test_remove_manual_entries_success_two_items():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160},
         {'Action': 'Entrada Manual', 'qtd': 5}]
    )
    mock_similarity = 85
    mock_manual_ref = ["entrada manual", "entrada digitada", "entrada do usuario", "input manual", "user input",
                       "input_inesperado"]
    mock_column = 'Action'
    
    result = remove_manual(mock_df, mock_manual_ref, mock_similarity, mock_column)
    expected_result = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_remove_manual_entries_success_five_items():
    mock_df = pd.DataFrame(
        [{'Action': 'muito_bom', 'qtd': 8313},
         {'Action': 'entrada manual', 'qtd': 2903},
         {'Action': 'nao_ajudou', 'qtd': 3642},
         {'Action': 'confuso', 'qtd': 1794},
         {'Action': 'lento', 'qtd': 581},
         {'Action': 'amei', 'qtd': 3465}]
    )
    mock_similarity = 85
    mock_manual_ref = ["entrada manual", "entrada digitada", "entrada do usuario", "input manual", "user input",
                       "input_inesperado"]
    mock_column = 'Action'
    
    result = remove_manual(mock_df, mock_manual_ref, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 'muito_bom', 'qtd': 8313},
         {'Action': 'nao_ajudou', 'qtd': 3642},
         {'Action': 'confuso', 'qtd': 1794},
         {'Action': 'lento', 'qtd': 581},
         {'Action': 'amei', 'qtd': 3465}]
    )
    
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result)


def test_remove_manual_entries_success_ten_items():
    mock_df = pd.DataFrame([
        {'Action': 1, 'qtd': 8313},
        {'Action': 2, 'qtd': 2903},
        {'Action': 3, 'qtd': 3642},
        {'Action': 4, 'qtd': 1794},
        {'Action': 5, 'qtd': 581},
        {'Action': 6, 'qtd': 3465},
        {'Action': 7, 'qtd': 3642},
        {'Action': 8, 'qtd': 1794},
        {'Action': 9, 'qtd': 581},
        {'Action': 10, 'qtd': 3465}]
    )
    
    mock_similarity = 85
    mock_manual_ref = ["entrada manual", "entrada digitada", "entrada do usuario", "input manual", "user input",
                       "input_inesperado"]
    mock_column = 'Action'
    
    result = remove_manual(mock_df, mock_manual_ref, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 1, 'qtd': 8313},
         {'Action': 2, 'qtd': 2903},
         {'Action': 3, 'qtd': 3642},
         {'Action': 4, 'qtd': 1794},
         {'Action': 5, 'qtd': 581},
         {'Action': 6, 'qtd': 3465},
         {'Action': 7, 'qtd': 3642},
         {'Action': 8, 'qtd': 1794},
         {'Action': 9, 'qtd': 581},
         {'Action': 10, 'qtd': 3465}]
    )
    
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected_result)


def test_remove_manual_entries_success_two_entries():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160},
         {'Action': 'Entrada Manual', 'qtd': 5},
         {'Action': 'input inesperado', 'qtd': 5}]
    )
    mock_similarity = 85
    mock_manual_ref = ["entrada manual", "entrada digitada", "entrada do usuario", "input manual", "user input",
                       "input_inesperado"]
    mock_column = 'Action'
    
    result = remove_manual(mock_df, mock_manual_ref, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)


def test_remove_manual_entries_success_no_entries():
    mock_df = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    mock_similarity = 85
    mock_manual_ref = ["entrada manual", "entrada digitada", "entrada do usuario", "input manual", "user input",
                       "input_inesperado"]
    mock_column = 'Action'
    
    result = remove_manual(mock_df, mock_manual_ref, mock_similarity, mock_column)
    
    expected_result = pd.DataFrame(
        [{'Action': 'Nao Ajudou', 'qtd': 200},
         {'Action': 'Ajudou', 'qtd': 160}]
    )
    
    pd.testing.assert_frame_equal(result, expected_result)
