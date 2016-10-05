from settings import GOOGLEMAP_API_KEY
import requests
import json

URL = "https://maps.googleapis.com/maps/api/geocode/json?address="
APIKEY = "&key=" + GOOGLEMAP_API_KEY



test_address = "1429 Sunnydale Ave"

req = requests.get(URL + test_address + APIKEY)
data = json.loads(req.text)

print(data)

results = data['results']

print(results)


