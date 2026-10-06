def rains_count(all_result) :
    rains = {}
    for result in all_result :
        rains[result['region_name']] = sum(result['daily']['rain_sum'])
    return rains

def average_rainfall(results):
    """Given multiple years' results for one region, return the average total rainfall."""
    totals = [sum(r["daily"]["rain_sum"]) for r in results]
    return sum(totals) / len(totals)


def drought_risk_score(current_total, historical_average):
    """Percent deficit vs. historical average. Positive = drier than normal."""
    if historical_average == 0:
        return 0.0
    return round((historical_average - current_total) / historical_average * 100, 1)