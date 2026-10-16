from datetime import date, timedelta
from statistics import mean, stdev


def rains_count(all_result):
    rains = {}
    for result in all_result:
        rains[result["region_name"]] = sum(result["daily"]["rain_sum"])
    return rains


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


def window_totals(years_data, start, end):
    """Rainfall total over the same calendar window in each past year.
    Years with any missing day are skipped."""
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
    return totals


def baseline_average(years_data, start, end):
    totals = window_totals(years_data, start, end)
    return sum(totals) / len(totals)


def baseline_stats(years_data, start, end):
    """Returns (mean, sample std, number of years used)."""
    totals = window_totals(years_data, start, end)
    if len(totals) < 2:
        raise ValueError("Need at least 2 baseline years for a standard deviation")
    return mean(totals), stdev(totals), len(totals)


def z_score(current, avg, std):
    if std == 0:
        return 0.0
    return round((current - avg) / std, 2)
