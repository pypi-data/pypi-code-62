import argparse
from unittest.mock import patch

import pytest
from fixtures import client
from freezegun import freeze_time
from cli_client import main

api_path = "/api/humantime"


# Test scenarios with invalid times
@pytest.mark.parametrize(
    "numeric_time",
    [
        "sometime",
        "123456",
        "Ten o' clock",
        "2500",
    ],
)
@patch("argparse.ArgumentParser.parse_args")
def test_get_change(cliargs, numeric_time):
    with pytest.raises(SystemExit, match="1"):
        cliargs.return_value = argparse.Namespace(**{"numeric_time": numeric_time})
        main()


# Test scenarios with different time formats
@pytest.mark.parametrize(
    "numeric_time",
    [
        "1:00",
        "01:00",
        "13:00",
        "13.00",
        "1300"
    ],
)
@patch("argparse.ArgumentParser.parse_args")
def test_with_different_time_formats(cliargs, numeric_time, capsys):
    with pytest.raises(SystemExit, match="0"):
        cliargs.return_value = argparse.Namespace(**{"numeric_time": numeric_time})
        main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "One o'clock"

# Test when not providing a time
@patch("argparse.ArgumentParser.parse_args")
def test_with_no_time(cliargs, capsys):
    with pytest.raises(SystemExit, match="0"):
        cliargs.return_value = argparse.Namespace(**{"numeric_time": "15:00"})
        main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Three o'clock"

@pytest.mark.parametrize(
    "numeric_time, expected_result",
    [
        ("00:00", "Twelve o'clock"),
        ("12:40", "Twenty to one"),
        ("13:00", "One o'clock"),
        ("13:11", "Eleven minutes past one"),
        ("13:15", "Quarter past one"),
        ("13:25", "Twenty five past one"),
        ("13:30", "Half past one"),
        ("13:32", "Twenty eight minutes to two"),
        ("13:35", "Twenty five to two"),
        ("13:45", "Quarter to two"),
        ("13:50", "Ten to two"),
        ("13:55", "Five to two"),
        ("13:57", "Three minutes to two"),
    ]
)
@patch("argparse.ArgumentParser.parse_args")
def test_get_change(cliargs, numeric_time, expected_result, capsys):
    with pytest.raises(SystemExit, match="0"):
        cliargs.return_value = argparse.Namespace(**{"numeric_time": numeric_time})
        main()
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result
