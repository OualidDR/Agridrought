from datetime import date
from dotenv import load_dotenv
from storage import download_json

load_dotenv()


def rank_by_dryness(scores):
    return sorted(scores.items(), key=lambda item: item[1]["drought_risk_pct"], reverse=True)


if __name__ == "__main__":
    today = date.today().isoformat()
    scores = download_json("gold", f"drought_index_{today}.json")
    ranked = rank_by_dryness(scores)
    for region, info in ranked:
      pct = info["drought_risk_pct"]
      label = f"{pct}% below normal" if pct >= 0 else f"{abs(pct)}% above normal"
      print(f"{region}: {label} ({info['current_mm']}mm vs {info['historical_avg_mm']}mm avg)")
    