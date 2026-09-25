from api import rains_count, fetch_all_regions_weather
from unittest.mock import patch, MagicMock

@patch("api.requests.get")

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

