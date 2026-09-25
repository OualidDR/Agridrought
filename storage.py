import json

def save_rains_json(rains) :
    with open ("rainfall_total.json", "w") as f :
        json.dump(rains, f, indent= 2)