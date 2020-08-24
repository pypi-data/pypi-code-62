"""
tests all functions in gameHub.py
"""
import filecmp
import json
try:
    from prompt_toolkit.terminal import win32_output
except ImportError:
    win32_output = None
from click.testing import CliRunner
from game_hub import gameHubCLI
from game_hub.gameHub import default_tic_config_path, default_gamehub_config_path
from game_hub.games.gameCLI import gamehub_config_path
from game_hub.games.ticTacToe import tic_config_path

gamehub_help_menu = """Usage: cli [OPTIONS] COMMAND [ARGS]...

  gamehub is an interface for the three games we currently have in stock,
  which are tictactoe, hangman and rock paper scissors. You can play these
  games by typing 'gamehub play [game]' you can see the names of the games by
  typing in 'gamehub play'. If you are in the repl, the commands are the same
  but you don't include the gamehub. As well as this , in the repl, you can
  press the tab key and a list of options appears that you can pick from.

Options:
  -h, --help  Show this message and exit.

Commands:
  generate   pick random game to play
  last_game  plays the last game you played
  play       group of all games
  play_list  play's a random game from a list
  repl       creates a repl and a exit command
  settings   The gamehub settings
"""
settings = """Usage: settings [OPTIONS] COMMAND [ARGS]...

  The gamehub settings

Options:
  --help  Show this message and exit.

Commands:
  tic  all the tictactoe_settings
"""
tic_settings = """Usage: tic [OPTIONS] COMMAND [ARGS]...

  all the tictactoe_settings

Options:
  --help  Show this message and exit.

Commands:
  pick_ai_mode  adds an ai mode to the tictactoe config
  reset         resets all settings to default
  tutorial      prints the tutorial
"""
tutorial = """You pick the slot you want to pick using a number. Each number
on the board corresponds to the number that you have to press
to pick that slot. The board looks like this:

    1  2  3
    4  5  6
    7  8  9

To win get three in a row

Here we'll show an example game so you don't get confused

Player one it's your turn!

Player one: 3

    1  2  X
    4  5  6
    7  8  9

Player 2 it's your turn!

Player 2: 6

    1  2  X
    4  5  O
    7  8  9

This continues until someone gets three in a row or they tie.
"""


def test_gamehub() -> None:
    """bruh"""
    runner = CliRunner()
    result = runner.invoke(gameHubCLI.cli)
    print('\n', result.exit_code)
    assert result.exit_code == 0
    assert result.output == gamehub_help_menu


def test_settings() -> None:
    """bruh"""
    runner = CliRunner()
    result = runner.invoke(gameHubCLI.settings)
    print('\n', result.exit_code)
    assert result.exit_code == 0
    assert result.output == settings


def test_tic_settings() -> None:
    """bruh"""
    runner = CliRunner()
    result = runner.invoke(gameHubCLI.tic_settings)
    print('\n', result.exit_code)
    assert result.exit_code == 0
    assert result.output == tic_settings


def test_pick_ai_mode() -> None:
    """bruh"""
    if win32_output is not None:
        runner = CliRunner()
        try:
            _ = runner.invoke(gameHubCLI.pick_ai_mode_cmd, catch_exceptions=False)
            assert False
        except win32_output.NoConsoleScreenBufferError:
            assert True
    else:
        assert True


def test_tutorial() -> None:
    """bruh"""
    runner = CliRunner()
    result = runner.invoke(gameHubCLI.tutorial_cmd)
    print(result.exit_code)
    assert result.exit_code == 0
    assert result.output == tutorial


def test_reset_settings() -> None:
    """bruh"""
    runner = CliRunner()
    file_paths = [tic_config_path, gamehub_config_path]
    for file_path in file_paths:
        with open(file_path, 'w') as config:
            json.dump({}, config, indent=2)
    runner.invoke(gameHubCLI.reset_settings_cmd, catch_exceptions=False)
    assert filecmp.cmp(tic_config_path, default_tic_config_path)
    assert filecmp.cmp(gamehub_config_path, default_gamehub_config_path)


def test_click_generate() -> None:
    """bruh"""
    if win32_output is not None:
        runner = CliRunner()
        try:
            _ = runner.invoke(gameHubCLI.generate_cmd, catch_exceptions=False)
            assert False
        except win32_output.NoConsoleScreenBufferError:
            assert True
    else:
        assert True


def test_play_again() -> None:
    """bruh"""
    if win32_output is not None:
        runner = CliRunner()
        try:
            _ = runner.invoke(gameHubCLI.play_again_cmd, catch_exceptions=False)
            assert False
        except win32_output.NoConsoleScreenBufferError:
            assert True
    else:
        assert True


def test_play_from_list() -> None:
    """bruh"""
    runner = CliRunner()
    if win32_output is not None:
        try:
            _ = runner.invoke(gameHubCLI.play_game_from_list_cmd, ['-g', 'tic', '-g', 'hang'], catch_exceptions=False)
            assert False
        except win32_output.NoConsoleScreenBufferError:
            assert True
    else:
        assert True


def test_create_repl() -> None:
    """bruh"""
    runner = CliRunner()
    try:
        _ = runner.invoke(gameHubCLI.create_repl_cmd, catch_exceptions=False)
        assert False
    except AttributeError:
        assert True
