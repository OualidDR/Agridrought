from fetch import fetch_all_regions_weather
from transform import rains_count
from storage import save_rains_json, load_to_azure_blob
regions = [
        {"name": "agadir", "latitude": 30.42, "longitude": -9.60},
        {"name": "marrakech", "latitude": 31.63, "longitude": -8.00},
        {"name": "casablanca", "latitude": 33.57, "longitude": -7.59},
        {"name": "tanger", "latitude": 35.77, "longitude": -5.80},
        {"name": "rabat", "latitude": 34.02, "longitude": -6.84},
        {"name": "fes", "latitude": 34.03, "longitude": -5.00},
        {"name": "ouarzazate", "latitude": 30.93, "longitude": -6.93},
        {"name": "tiznit", "latitude": 29.70, "longitude": -9.73},
        {"name": "taroudant", "latitude": 30.47, "longitude": -8.88},
        {"name": "errachidia", "latitude": 31.93, "longitude": -4.42}
    ]

def main():
    all_result = fetch_all_regions_weather(regions)
    total_rains = rains_count(all_result)
    save_rains_json(total_rains)
    load_to_azure_blob("rainfall_total.json", "rainfall_total.json")

if __name__ == "__main__":
    main()