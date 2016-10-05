import json

import requests

from craigslist_apt.settings import GOOGLEMAP_API_KEY

URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
APIKEY = "&key=" + GOOGLEMAP_API_KEY


def get_lat_lon(address):
    req = requests.get(URL + address + APIKEY)
    data = json.loads(req.text)

    status = data['status']

    if status == 'OK':
        results = data['results'][0]
        formal_address = results['formatted_address']
        lat = results['geometry']['location']['lat']
        lon = results['geometry']['location']['lng']

        return formal_address, lat, lon


if __name__ == "__main__":
    test_address = "1429 Sunnydale Ave"
    print(get_lat_lon(test_address))
