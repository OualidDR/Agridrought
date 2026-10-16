from datetime import date
from config import BASELINE_BLOB
from storage import download_json, upload_json
from transform import rains_count, baseline_stats, drought_risk_score, z_score


def main():
    today = date.today().isoformat()
    current = download_json("bronze", f"openmeteo/current/{today}.json")
    baseline = download_json("bronze", BASELINE_BLOB)

    totals = rains_count(current)
    scores = {}
    for item in current:
        name = item["region_name"]
        times = item["daily"]["time"]
        start, end = date.fromisoformat(times[0]), date.fromisoformat(times[-1])
        avg, std, n_years = baseline_stats(baseline[name], start, end)
        scores[name] = {
            "window": f"{times[0]} to {times[-1]}",
            "current_mm": round(totals[name], 2),
            "historical_avg_mm": round(avg, 2),
            "drought_risk_pct": drought_risk_score(totals[name], avg),
            "z_score": z_score(totals[name], avg, std),
            "baseline_years": n_years,
        }
    upload_json("gold", f"drought_index_{today}.json", scores)


if __name__ == "__main__":
    main()
