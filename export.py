from pprint import pprint

import pymongo

mongo = pymongo.MongoClient()

low_price = 1500
high_price = 2300

bedroom = 1
conditions = {
    'price': {
        '$gte': str(low_price),
        '$lte': str(high_price)
    },
    'bedroom': str(bedroom)
}

result = mongo.apt.craigslist.find(conditions)

for i in result:
    pprint(i)
