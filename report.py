import json
import os 
from dotenv import load_dotenv

load_dotenv()

def load_rains(filename):
    with open(filename) as f:
        return json.load(f)

def rank_by_dryness(rains):
    # return regions sorted from driest (lowest rainfall) to wettest
    return sorted(rains.items(), key=lambda item: item[1])

if __name__ == "__main__":
    from storage import download_from_blob
    download_from_blob("rainfall_total.json", "rainfall_total.json")
    rains = load_rains("rainfall_total.json")
    ranked = rank_by_dryness(rains)
    for region, total in ranked:
        print(f"{region}: {round(total, 2)} mm")