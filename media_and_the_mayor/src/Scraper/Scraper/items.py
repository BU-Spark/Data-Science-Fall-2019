# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Article(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	date = scrapy.Field()
	journal = scrapy.Field()
	author = scrapy.Field()
	category = scrapy.Field()
	page_number = scrapy.Field()
	summary = scrapy.Field()
	body = scrapy.Field()
	source = scrapy.Field()
	media = scrapy.Field()
	tags = scrapy.Field()


class WaybackDates(scrapy.Item):
	date = scrapy.Field()