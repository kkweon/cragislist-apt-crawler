import json
from pprint import pprint

import requests

from craigslist_apt import settings
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


def get_address_by_lat_lon(lat, lon):
    #https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY
    URL = "https://maps.googleapis.com/maps/api/geocode/json?latlng="
    URL = URL + str(lat) + "," + str(lon) + APIKEY

    req = requests.get(URL)
    data = json.loads(req.text)

    status = data['status']
    if status == "OK":
        results = data['results'][0]
        formal_address = results['formatted_address']
        lat = results['geometry']['location']['lat']
        lon = results['geometry']['location']['lng']

        return formal_address, lat, lon

    else:
        print(status)


if __name__ == "__main__":
    test_address = "3800 north el mirage rd"

    test_lat = settings.WORK_LAT
    test_lon = settings.WORK_LON

    pprint(get_address_by_lat_lon(test_lat, test_lon))
