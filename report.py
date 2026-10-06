import json
import os 
from dotenv import load_dotenv

load_dotenv()

def load_rains(filename):
    with open(filename) as f:
        return json.load(f)

def rank_by_dryness(rains):
    return sorted(rains.items(), key=lambda item: item[1]["drought_risk_pct"], reverse=True)

if __name__ == "__main__":
    from storage import download_from_blob
    download_from_blob("drought_index.json", "drought_index.json")
    rains = load_rains("drought_index.json")
    ranked = rank_by_dryness(rains)
    for region, info in ranked:
        print(f"{region}: {info['drought_risk_pct']}% below normal "
      f"({round(info['current_mm'], 2)}mm vs {info['historical_avg_mm']}mm avg)")