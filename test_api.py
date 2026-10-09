from transform import rains_count
from fetch import fetch_all_regions_weather
from unittest.mock import patch, MagicMock
from datetime import date 
from transform import baseline_average
import pytest

fake_baseline = {
    "2024": {"time": ["2024-10-01", "2024-10-02", "2024-10-03"], "rain_sum": [1.0, 2.0, 3.0]},
    "2025": {"time": ["2025-10-01", "2025-10-02", "2025-10-03"], "rain_sum": [0.0, 0.0, 4.0]},
}

@patch("fetch.requests.get")

def test_fetch_all_regions_weather(mock_get) :
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "latitude": 30.0, "longitude": -9.0,
        "daily": {"time": ["2026-09-08"], "rain_sum": [1.5]}
    }
    mock_get.return_value = mock_response

    regions = [{"name": "agadir", "latitude": 30.42, "longitude": -9.60}]
    result = fetch_all_regions_weather(regions)

    assert result[0]["region_name"] == "agadir"
    assert result[0]["daily"]["rain_sum"] == [1.5]
    mock_get.assert_called_once()



def test_rains_count() :
    fake_all_result = [
        {
        "region_name": "testville",
        "daily": {"rain_sum": [1.0, 2.0, 3.0]}
         },
        {
        "region_name": "otherplace",
        "daily": {"rain_sum": [0.0, 0.0, 5.5]}
        },
    ]   
    result = rains_count(fake_all_result)
    assert result == {"testville" : 6.0, "otherplace" : 5.5}

def test_baseline_average_normal():
    # 2024 totals 6.0, 2025 totals 4.0 -> average 5.0
    result = baseline_average(fake_baseline, date(2026, 10, 1), date(2026, 10, 3))
    assert result == 5.0


def test_baseline_average_skips_incomplete_year():
    data = {
        **fake_baseline,
        "2023": {"time": ["2023-10-01", "2023-10-02"], "rain_sum": [9.0, 9.0]},  # day 3 missing
    }
    result = baseline_average(data, date(2026, 10, 1), date(2026, 10, 3))
    assert result == 5.0  # the partial year must not drag the average up


def test_baseline_average_no_usable_data():
    with pytest.raises(ValueError):
        baseline_average({}, date(2026, 10, 1), date(2026, 10, 3))