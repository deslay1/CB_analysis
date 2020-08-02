import csv

# Methods for obtaining repo rates.

def getAllExchangeRates(client, aggregate_method, date_from, date_to, only_average, groups_id, currency):

    groups = getRiskbankKeyInterestRatesGroups(client, groups_id, "en")
    single_group_id = groups[0].groupid
    key_interest_rates_series = getKeyInterestRates(client, single_group_id, "en")

    exchange_rates_info = getExchangeRates(key_interest_rates_series, currency)

    searchRequestParameters = getSearchRequestParameters(aggregate_method, date_from, date_to, "en", not only_average, only_average,
                                                        not only_average, not only_average, single_group_id,
                                                        exchange_rates_info.seriesid)
    exchange_rates_series = client.service.getInterestAndExchangeRates(searchRequestParameters)

    exchanges_rates_name = exchange_rates_series.groups[0].groupname

    #printExchangeRatesWithDates(exchange_rates_series)

    write_to_csv(exchange_rates_series, aggregate_method)

    return exchange_rates_info, groups[0].groupname

def getRiskbankKeyInterestRatesGroups(client, group_id, language):
    response = client.service.getInterestAndExchangeGroupNames(language)
    return [group for group in response if group.groupid == group_id]


def getKeyInterestRates(client, key_interest_group, language):
    return client.service.getInterestAndExchangeNames(key_interest_group, language)


def getExchangeRates(key_interest_rates_series, currency):
    for series in key_interest_rates_series:
        if series.shortdescription == currency:
            return series


def getSearchGroupSeries(group, series):
    return {"groupid": group, "seriesid": series}


def getSearchRequestParameters(method, date_from, date_to, language, min, avg, max, ultimo, group, series):
    return {"aggregateMethod": method, "datefrom": date_from, "dateto": date_to,
            "languageid": language, "min": min, "avg": avg, "max": max, "ultimo": ultimo,
            "searchGroupSeries": getSearchGroupSeries(group, series)}


# Debug purposes for average values
def printExchangeRatesWithDates(exchange_rates_series):
    for obs in exchange_rates_series.groups[0].series[0].resultrows:
        print("Exchange rates: " + obs.date.strftime("%d-%b-%Y") + ": " + str(obs.average))


def write_to_csv(data_series, aggregate_method):
    observations = data_series.groups[0].series[0].resultrows
    print(observations)
    with open('exchange_rates.csv', 'w', ) as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Average', 'Min', 'Max', 'Ultimo'])
        for obs in observations:
            if obs.average is not None:
                #writer.writerow([obs.date.strftime("%d-%b-%Y"), obs.average, obs.min, obs.max, obs.ultimo])
                writer.writerow([obs.date.strftime("%d-%b-%Y"), obs.average, obs.min, obs.max, obs.ultimo])