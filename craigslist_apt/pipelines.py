# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from datetime import datetime

import pymongo as pymongo

from craigslist_apt import settings
from craigslist_apt.caltrain_stops import *

CALTRAIN_DATA = read_data()


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings.MONGODB_SERVER,
            settings.MONGODB_PORT
        )
        db = connection[settings.MONGODB_DB]
        self.collection = db[settings.MONGODB_COLLECTION]

        self.logger = logging.getLogger("cl_logger")

    def process_item(self, item, spider):
        # for data in item:
        #     if not data:
        #         raise DropItem("Missing data!")
        data = dict(item)
        data['update_date'] = datetime.now()
        if 'lat' in data.keys() and 'lon' in data.keys():
            if data['lat'] is not None and data['lon'] is not None:
                data['address'], data['caltrain_stop'], data['caltrain_dist'] = get_closest_caltrain_by_lat_lon(CALTRAIN_DATA, data['lat'], data['lon'])
                data['work_dist'] = get_distance_from_work(data['lat'], data['lon'])
        self.collection.update({'link': data['link']}, data, upsert=True)
        self.logger.info("Added to MongoDB database!")

        return data
