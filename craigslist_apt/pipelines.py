# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo as pymongo
#from scrapy.exceptions import DropItem
import logging
from datetime import datetime

from craigslist_apt import settings


class CraigslistAptPipeline(object):
    def process_item(self, item, spider):
        return item

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
        self.collection.update({'link': data['link']}, data, upsert=True)
        self.logger.info("Added to MongoDB database!")
        return item