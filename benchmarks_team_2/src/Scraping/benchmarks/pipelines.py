# -*- coding: utf-8 -*-
import pymongo

from scrapy import settings
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class BenchmarksPipeline(object):
#     def process_item(self, item, spider):
#         return item

class MongoDBPipeline(object):

    # def __init__(self):
    #     connection = pymongo.MongoClient(
    #         settings['MONGODB_SERVER'],
    #         settings['MONGODB_PORT']
    #     )
    #     db = connection[settings['MONGODB_DB']]
    #     self.collection = db[settings['MONGODB_COLLECTION']]
    collection_name = 'sjc_opinions'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'tc_scraper')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
        return item