import requests


def search_serial(serial_name):
    params = {'q': serial_name}
    result = requests.get('http://api.tvmaze.com/search/shows', params=params)
    result.raise_for_status()

    return result.json()
