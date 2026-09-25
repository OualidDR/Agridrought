def rains_count(all_result) :
    rains = {}
    for result in all_result :
        rains[result['region_name']] = sum(result['daily']['rain_sum'])
    return rains