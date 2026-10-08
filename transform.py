from datetime import date, timedelta

def rains_count(all_result) :
    rains = {}
    for result in all_result :
        rains[result['region_name']] = sum(result['daily']['rain_sum'])
    return rains

def average_rainfall(results):
    totals = [sum(r["daily"]["rain_sum"]) for r in results]
    if not totals:
        raise ValueError("No baseline data available, cannot compute average")
    return sum(totals) / len(totals)


def drought_risk_score(current_total, historical_average):
    """Percent deficit vs. historical average. Positive = drier than normal."""
    if historical_average == 0:
        return 0.0
    return round((historical_average - current_total) / historical_average * 100, 1)

def shift_year(d, year):
    try:
        return d.replace(year=year)
    except ValueError:  # Feb 29 in a non-leap year
        return d.replace(year=year, day=28)


def baseline_average(years_data, start, end):
    """Average rainfall over the same calendar window (start..end) in each past year."""
    lookup = {}
    for daily in years_data.values():
        for t, mm in zip(daily["time"], daily["rain_sum"]):
            if mm is not None:
                lookup[date.fromisoformat(t)] = mm

    span = (end - start).days
    totals = []
    for year in years_data:
        e = shift_year(end, int(year))
        days = [e - timedelta(days=i) for i in range(span + 1)]
        if all(d in lookup for d in days):
            totals.append(sum(lookup[d] for d in days))

    if not totals:
        raise ValueError("No complete baseline year covers this window")
    return sum(totals) / len(totals)