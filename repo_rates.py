import csv

# Methods for obtaining repo rates.

def getAllRepoRates(client, aggregate_method, date_from, date_to, only_average, groups_id):

    groups = getRiskbankKeyInterestRatesGroups(client, groups_id, "en")
    single_group_id = groups[0].groupid
    key_interest_rates_series = getKeyInterestRates(client, single_group_id, "en")

    repo_rates_info = getRepoRates(key_interest_rates_series)

    searchRequestParameters = getSearchRequestParameters(aggregate_method, date_from, date_to, "en", not only_average, only_average,
                                                         not only_average, not only_average, single_group_id,
                                                         repo_rates_info.seriesid)
    repo_rates_series = client.service.getInterestAndExchangeRates(searchRequestParameters)
    repo_rates_name = repo_rates_series.groups[0].groupname

    #printRepoRatesWithDates(repo_rates_series)

    write_to_csv(repo_rates_series)

    return repo_rates_info, groups[0].groupname

def getRiskbankKeyInterestRatesGroups(client, parent_group_id, language):
    response = client.service.getInterestAndExchangeGroupNames(language)
    return [group for group in response if group.parentgroupid == parent_group_id]


def getKeyInterestRates(client, key_interest_group, language):
    return client.service.getInterestAndExchangeNames(key_interest_group, language)


def getRepoRates(key_interest_rates_series):
    for series in key_interest_rates_series:
        if series.description == "Repo rate":
            return series


def getSearchGroupSeries(group, series):
    return {"groupid": group, "seriesid": series}


def getSearchRequestParameters(method, date_from, date_to, language, min, avg, max, ultimo, group, series):
    return {"aggregateMethod": method, "datefrom": date_from, "dateto": date_to,
            "languageid": language, "min": min, "avg": avg, "max": max, "ultimo": ultimo,
            "searchGroupSeries": getSearchGroupSeries(group, series)}


# Debug purposes for average values
def printRepoRatesWithDates(repo_rates_series):
    print("Repo rates: ")
    # Why arrays[0]? --> Because the api returns an array even if it for sure only contains only one object.
    for obs in repo_rates_series.groups[0].series[0].resultrows:
        print("Repo rate: " + obs.date.strftime("%d-%b-%Y") + ": " + str(obs.average))


def write_to_csv(data_series):
    observations = data_series.groups[0].series[0].resultrows
    with open('repo_rates.csv', 'w', ) as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Average', 'Min', 'Max', 'Ultimo'])
        for obs in observations:
            if obs.average is not None:
                #writer.writerow([obs.date.strftime("%d-%b-%Y"), obs.average, obs.min, obs.max, obs.ultimo])
                writer.writerow([obs.date.strftime("%d-%b-%Y"), obs.average, obs.min, obs.max, obs.ultimo])
