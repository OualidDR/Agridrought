from fetch import fetch_all_regions_weather, fetch_historical_baseline
from transform import rains_count, average_rainfall, drought_risk_score
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
    current_totals = rains_count(all_result)

    drought_scores = {}
    for region in regions:
        baseline_results = fetch_historical_baseline(
            region, "09-08", "09-22", years=[2021, 2022, 2023, 2024]
        )
        avg = average_rainfall(baseline_results)
        score = drought_risk_score(current_totals[region["name"]], avg)
        drought_scores[region["name"]] = {
            "current_mm": current_totals[region["name"]],
            "historical_avg_mm": round(avg, 2),
            "drought_risk_pct": score,
        }

    save_rains_json(drought_scores, filename="drought_index.json")
    load_to_azure_blob("drought_index.json", "drought_index.json")

if __name__ == "__main__":
    main()