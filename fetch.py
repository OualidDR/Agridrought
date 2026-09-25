import requests


url ="https://archive-api.open-meteo.com/v1/archive"

# i make a list of dics
regions = [
    {"name" : 'agadir', 'latitude' : 30.42, 'longitude' : -9.60},
    {"name" : 'marrakech', 'latitude' : 31.63, 'longitude' : -8.00},
    {"name" : 'casablanca', 'latitude' : 33.58, 'longitude' : -7.61},
]
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
        response = requests.get(url, params=params)
    #  store the result in a list 
        data = response.json()
        data["region_name"] = region["name"]
        all_result.append(data)
    return all_result