"""
tests all functions in gameHub.py
"""
import filecmp
import json
import pytest
try:
    from prompt_toolkit.terminal import win32_output
except ImportError:
    win32_output = None


from test.test_game.test_ticTacToe import test_data_root
from game_hub import gameHub
from game_hub.games import hangMan, rockPaperScissors, ticTacToe

list_games = [rockPaperScissors.rps_game, hangMan.game, ticTacToe.game]

create_config_dir = test_data_root / 'dir_create_config'


def test_pick_ai_mode() -> None:
    """
    tests the pick_ai_mode() function
    """
    if win32_output is not None:
        try:
            gameHub.pick_ai_mode()
            assert False
        except win32_output.NoConsoleScreenBufferError:
            assert True
    else:
        assert True


def test_create_repl() -> None:
    """
    tests the pick_ai_mode() function
    """
    try:
        gameHub.create_repl()
        assert False
    except RuntimeError:
        assert True


def test_create_config() -> None:
    """
    tests the create_config()
    """
    dst = create_config_dir / 'dst_create_config.json'
    src = create_config_dir / 'src_create_config.json'
    default_src_config = {"one": 1}
    default_dst_config = {}

    with open(dst, 'w') as dst_file:
        json.dump(default_dst_config, dst_file, indent=4)
    with open(src, 'w') as src_file:
        json.dump(default_src_config, src_file, indent=4)

    gameHub.create_config(src, dst, reset=True)
    assert filecmp.cmp(dst, src)


def test_generate() -> None:
    """
    tests generate() function by making two lists of randomly generated games. Then it tests if the results are games
    and not just any random value. If they aren't games, then it fails. Finally it tests if the randomly generated lists
    aren't the same. If they are the same, then it fails.
    """
    random_results_1 = []
    random_results_2 = []
    for _ in range(9):
        random_results_1.append(gameHub.generate())
        random_results_2.append(gameHub.generate())
    for random_result_1 in random_results_1:
        assert random_result_1 in list_games
    for random_result_2 in random_results_2:
        assert random_result_2 in list_games
    assert random_results_1 != random_results_2


@pytest.mark.parametrize("games,expected", [
    (['tic', 'hang'], ['tictactoe', 'hangman']),
    (['rps', 'hang'], ['rps', 'hangman']),
    (['tic', 'rps'], ['tictactoe', 'rps']),
])
def test_pick_rand_game(games: list, expected: list) -> None:
    """
    tests play_random_game_from_list() function in gameHub.py
    """
    actual_output = gameHub.pick_rand_game(list(games))
    random_results_1 = []
    random_results_2 = []
    assert actual_output in expected
    for _ in range(20):
        random_results_1.append(gameHub.pick_rand_game(list(games)))
        random_results_2.append(gameHub.pick_rand_game(list(games)))
    assert random_results_1 != random_results_2


def test_play_again() -> None:
    """
    tests the play_again() function
    """
    last_game_path = test_data_root / 'test_last_game.json'
    # noinspection PyNoneFunctionAssignment
    last_game = gameHub.play_again(last_game_path)
    assert last_game == 1
