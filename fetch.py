import requests
import time

url ="https://archive-api.open-meteo.com/v1/archive"

# i make a list of dics

    
def fetch_all_regions_weather (regions) :
     all_result = []
     for region in regions:
        params = {
            "latitude": region['latitude'],
            "longitude": region['longitude'],
            "start_date": "2026-09-08",
            "end_date": "2026-09-22",
            'timezone': 'auto',
            "daily": "rain_sum"
        }
        response = requests.get(url, params=params, timeout=10)
    #  store the result in a list 
        data = response.json()
        data["region_name"] = region["name"]
        all_result.append(data)
     return all_result

def fetch_region_weather_for_year(region, start_date, end_date, retries=3):
    params = {...}  # unchanged
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
            time.sleep(2 ** attempt)  # wait 1s, 2s, then give up


def fetch_historical_baseline(region, month_day_start, month_day_end, years):
    results = []
    for year in years:
        start = f"{year}-{month_day_start}"
        end = f"{year}-{month_day_end}"
        try:
            results.append(fetch_region_weather_for_year(region, start, end))
        except requests.exceptions.RequestException:
            print(f"Skipping {region['name']} {year}: request failed")
        time.sleep(0.5)
    return results