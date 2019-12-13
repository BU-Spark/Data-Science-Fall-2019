# -*- coding: utf-8 -*-
from Scrapy.exceptions import DropItem
import re



class ScraperPipeline(object):
    def process_item(self, item, spider):
    	if item['date']:
    		pass

    	if not item['body']:
    		raise DropItem("Body not found in ", item)
        
        return item
