import pytest
from unittest.mock import patch, MagicMock
from src.extract.usgs_client import fetch_earthquakes, parse_feature


SAMPLE_FEATURE = {
    "id": "us7000abc1",
    "properties": {
        "mag": 5.2,
        "place": "42 km SSW of Nazca, Peru",
        "time": 1700000000000,
        "magType": "mww",
        "status": "reviewed",
        "tsunami": 0,
        "felt": 15,
        "sig": 416,
    },
    "geometry": {
        "coordinates": [-75.12, -15.23, 35.0],
    },
}


def _mock_response(features):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"features": features}
    resp.raise_for_status.return_value = None
    return resp


@patch("src.extract.usgs_client.requests.get")
def test_fetch_returns_features(mock_get):
    mock_get.return_value = _mock_response([SAMPLE_FEATURE])
    result = fetch_earthquakes("2024-01-01", "2024-01-31")
    assert len(result) == 1
    assert result[0]["id"] == "us7000abc1"


@patch("src.extract.usgs_client.requests.get")
def test_fetch_empty(mock_get):
    mock_get.return_value = _mock_response([])
    result = fetch_earthquakes("2024-01-01", "2024-01-31")
    assert result == []


@patch("src.extract.usgs_client.requests.get")
def test_fetch_retry_on_error(mock_get):
    import requests as req
    mock_get.side_effect = [
        req.exceptions.ConnectionError("timeout"),
        _mock_response([SAMPLE_FEATURE]),
    ]
    result = fetch_earthquakes("2024-01-01", "2024-01-31")
    assert len(result) == 1


@patch("src.extract.usgs_client.requests.get")
def test_fetch_max_retries(mock_get):
    import requests as req
    mock_get.side_effect = req.exceptions.ConnectionError("fallo")
    with pytest.raises(ConnectionError):
        fetch_earthquakes("2024-01-01", "2024-01-31")


def test_parse_feature():
    parsed = parse_feature(SAMPLE_FEATURE)
    assert parsed["id_usgs"] == "us7000abc1"
    assert parsed["magnitud"] == 5.2
    assert parsed["latitud"] == -15.23
    assert parsed["longitud"] == -75.12
    assert parsed["profundidad_km"] == 35.0
    assert parsed["tsunami"] == 0


def test_parse_feature_missing_coords():
    feature = {
        "id": "test1",
        "properties": {"mag": 3.0, "place": "test", "time": 1700000000000},
        "geometry": {"coordinates": []},
    }
    parsed = parse_feature(feature)
    assert parsed["latitud"] is None
