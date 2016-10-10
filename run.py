import pymongo
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import craigslist_apt.settings as settings


class Database(object):
    def __init__(self):
        conn = pymongo.MongoClient(settings.MONGODB_SERVER, settings.MONGODB_PORT)
        self.db = conn[settings.MONGODB_DB]

    def remove(self, collection):
        self.db.drop_collection(collection)


def main():
    MongoDB = Database()
    MongoDB.remove(settings.MONGODB_COLLECTION)
    process = CrawlerProcess(get_project_settings())
    process.crawl('cl')
    process.start()


if __name__ == '__main__':
    main()
