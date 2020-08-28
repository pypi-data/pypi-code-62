import pytest
from fixtures import client
from freezegun import freeze_time

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
def test_with_invalid_times(client, numeric_time):
    result = client.get("{}?numeric_time={}".format(api_path, numeric_time))
    body = result.json

    assert result.status_code == 400
    assert body["errorMessage"] is not None


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
def test_with_different_time_formats(client, numeric_time):
    result = client.get("{}?numeric_time={}".format(api_path, numeric_time))
    body = result.json
    assert result.status_code == 200
    assert body["humanTime"] == "One o'clock"


# Test scenarios with different time formats
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
    ],
)
def test_with_different_times(client, numeric_time, expected_result):
    result = client.get("{}?numeric_time={}".format(api_path, numeric_time))
    body = result.json
    assert result.status_code == 200
    assert body["humanTime"] == expected_result


# Test when not providing a time
def test_with_no_time(client):
    with freeze_time("2020-08-26 15:00:00.000000"):
        result = client.get(api_path)
        body = result.json
        assert result.status_code == 200
        assert body["humanTime"] == "Three o'clock"
