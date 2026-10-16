from datetime import date
from config import BASELINE_BLOB, BASELINE_YEARS
from regions import regions
from fetch import fetch_all_regions_weather, fetch_full_years
from storage import upload_json, get_blob_client


def main():
    today = date.today().isoformat()
    raw_current = fetch_all_regions_weather(regions)
    upload_json("bronze", f"openmeteo/current/{today}.json", raw_current)

    if not get_blob_client("bronze", BASELINE_BLOB).exists():
        baseline = {r["name"]: fetch_full_years(r, BASELINE_YEARS) for r in regions}
        upload_json("bronze", BASELINE_BLOB, baseline)


if __name__ == "__main__":
    main()
