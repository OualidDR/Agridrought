import requests
import json


url ="https://archive-api.open-meteo.com/v1/archive"

# i make a list of dics
regions = [
    {"name" : 'agadir', 'latitude' : 30.42, 'longitude' : -9.60},
    {"name" : 'marrakech', 'latitude' : 31.63, 'longitude' : -8.00},
    {"name" : 'casablanca', 'latitude' : 33.58, 'longitude' : -7.61},
]

#  loop on this list and make a get 
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


rains = {}
for result in all_result :
    rains[result['region_name']] = sum(result['daily']['rain_sum'])

print(rains)
with open ("rainfall_total.json", "w") as f :
    json.dump(rains, f, indent= 2)