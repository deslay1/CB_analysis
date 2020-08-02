

# 137: Riksbank interest rates
# 130: Currencies against Swedish kronor


def print_response(client, language):
    response = client.service.getInterestAndExchangeGroupNames(language)
    print(response)