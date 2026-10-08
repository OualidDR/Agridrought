from datetime import date
from storage import download_json, upload_json
from transform import rains_count, average_rainfall, drought_risk_score

def main():
    today = date.today().isoformat()
    current = download_json("bronze", f"openmeteo/current/{today}.json")
    baseline = download_json("bronze", "openmeteo/baseline/baseline.json")
    totals = rains_count(current)
    scores = {}
    for name, total in totals.items():
        avg = average_rainfall(baseline[name])
        scores[name] = {
            "current_mm": round(total, 2),
            "historical_avg_mm": round(avg, 2),
            "drought_risk_pct": drought_risk_score(total, avg),
        }
    upload_json("gold", f"drought_index_{today}.json", scores)

if __name__ == "__main__":
    main()