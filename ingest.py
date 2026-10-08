from datetime import date
from regions import regions
from fetch import fetch_all_regions_weather, fetch_historical_baseline
from storage import upload_json, get_blob_client

def main():
    today = date.today().isoformat()
    raw_current = fetch_all_regions_weather(regions)
    upload_json("bronze", f"openmeteo/current/{today}.json", raw_current)

    if not get_blob_client("bronze", "openmeteo/baseline/baseline.json").exists():
        baseline = {
            r["name"]: fetch_historical_baseline(r, "09-08", "09-22", [2021, 2022, 2023, 2024])
            for r in regions
        }
        upload_json("bronze", "openmeteo/baseline/baseline.json", baseline)

if __name__ == "__main__":
    main()