import time
from datetime import date, timedelta

import requests

url = "https://archive-api.open-meteo.com/v1/archive"

LAG_DAYS = 5  # the archive API lags a few days behind real time


def current_window():
    end = date.today() - timedelta(days=LAG_DAYS)
    start = end - timedelta(days=13)
    return start.isoformat(), end.isoformat()


def fetch_region_weather_for_year(region, start_date, end_date, retries=3):
    params = {
        "latitude": region["latitude"],
        "longitude": region["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "daily": "rain_sum",
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            data["region_name"] = region["name"]
            return data
        except requests.exceptions.RequestException:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)


def fetch_all_regions_weather(regions):
    start, end = current_window()
    return [fetch_region_weather_for_year(r, start, end) for r in regions]


def fetch_full_years(region, years):
    """Full daily series per year, e.g. {"2021": {"time": [...], "rain_sum": [...]}, ...}"""
    result = {}
    for y in years:
        data = fetch_region_weather_for_year(region, f"{y}-01-01", f"{y}-12-31")
        result[str(y)] = data["daily"]
        time.sleep(0.5)
    return result