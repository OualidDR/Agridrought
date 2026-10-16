from datetime import date
from dotenv import load_dotenv
from storage import download_json

load_dotenv()


def rank_by_dryness(scores):
    # most negative z-score = driest relative to normal
    return sorted(scores.items(), key=lambda item: item[1]["z_score"])


if __name__ == "__main__":
    today = date.today().isoformat()
    scores = download_json("gold", f"drought_index_{today}.json")
    for region, info in rank_by_dryness(scores):
        pct = info["drought_risk_pct"]
        label = f"{pct}% below normal" if pct >= 0 else f"{abs(pct)}% above normal"
        print(f"{region}: z={info['z_score']:+.2f} | {label} "
              f"({info['current_mm']}mm vs {info['historical_avg_mm']}mm avg, "
              f"{info['baseline_years']} yrs)")
