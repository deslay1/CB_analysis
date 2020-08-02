from zeep import Client
from repo_rates import getAllRepoRates
from exchange_rates import getAllExchangeRates
from print_response import print_response
from graphs import visualize_observations, read_from_csv


def main():
    client = Client('https://swea.riksbank.se/sweaWS/wsdl/sweaWS_ssl.wsdl')
    # Use the following command to inspect file
    # python -mzeep https://swea.riksbank.se/sweaWS/wsdl/sweaWS_ssl.wsdl

    # Use the following to find out what group IDs are included in the API:
    # print_response(client, "en")

    only_average = True
    currency = "USD"
    aggregate_method = "Y"

    repo_rates_info, repo_rates_group_name = getAllRepoRates(client, aggregate_method , "1994-01-01", "2020-01-01",
                                                             only_average=only_average, groups_id=137)
    exchange_rates_info, exchange_rates_group_name = getAllExchangeRates(client, aggregate_method, "1994-01-01", "2020-01-01",
                                                                         only_average=only_average,
                                                                         groups_id=130, currency=currency)

    repo_rates_dates, repo_rates_values = read_from_csv('repo_rates.csv', only_average=only_average)
    exchange_rates_dates, exchange_rates_values = read_from_csv('exchange_rates.csv', only_average=only_average)
    visualize_observations(repo_rates_dates, [repo_rates_values, exchange_rates_values],
                           [repo_rates_info, exchange_rates_info], [repo_rates_group_name, exchange_rates_group_name],
                           only_average=only_average)


if __name__ == "__main__":
    main()
