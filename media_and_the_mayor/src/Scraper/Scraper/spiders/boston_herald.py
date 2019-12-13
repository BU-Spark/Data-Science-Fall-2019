# -*- coding: utf-8 -*-
import scrapy
from Scraper.items import Article

import re
from datetime import datetime



class BostonHeraldSpider(scrapy.Spider):
	name = 'boston_herald'
	
	allowed_domains = ['www.bostonherald.com']
	start_urls = ['https://www.bostonherald.com']


	def __init__(self, start_year=0, *args, **kwargs):
		super(BostonHeraldSpider, self).__init__(*args, **kwargs)

		self.start_year = start_year


	def parse(self, response):
		categories = response.css('ul#primary-menu ul.sub-menu li a::attr(href)').getall()

		for category_url in categories:
			if not category_url.startswith(self.start_urls[0]):
				category_url = self.start_urls[0] + category_url

			yield scrapy.Request(
				url = category_url, 
				callback = self.parse_categories
			)


	def parse_categories(self, response):
		next_page = response.css('a.load-more::attr(href)').get()


		if next_page is not None or '/page/' in response.url:
			articles = response.css('div.article-info a.article-title::attr(href)').getall()

			last_date_selector = response.css('div#page div#content div.tag-content article:last-of-type div.article-info time::text').get()
			last_date = int(last_date_selector.split(' ')[2])

			if next_page:
				regex = re.search(r'^' + re.escape(self.start_urls[0]) + r'/(.+?)/page.*', next_page)
			else:
				regex = re.search(r'^' + re.escape(self.start_urls[0]) + r'/(.+?)/page.*', response.url)
			
			categories_tags = regex.group(1).split('/')

			for article_url in articles:
				yield scrapy.Request(
					url = article_url, 
					callback = self.parse_article, 
					meta = {
						'category' : categories_tags
					}
				)

			if last_date >= self.start_year:
				yield scrapy.Request(
					url = next_page, 
					callback = self.parse_categories
				)


	def parse_article(self, response):
		article = Article()

		scraped_datetime = response.css('div.meta div.time time::attr(datetime)').get()
		year = int(scraped_datetime.split('-')[0])


		if year >= self.start_year:
			article['url'] = response.url
			
			article['title'] = response.css('head title::text').get()
			
			article['date'] = scraped_datetime
			
			article['journal'] = 'Boston Herald'

			article['author'] = response.css('div#page div#content article div.article-content div.header-features div.meta div.byline a.author-name::text').get()
			
			article['category'] = response.meta['category']

			article['summary'] = response.css('head meta[name="description"]::attr(content)').get()
			
			article['body'] = ' '.join(response.css('div.body-copy p::text').getall())
			
			article['tags'] = response.css('div.tags ul li a::text').getall()

			article['media'] = response.css('div#content main#main article div.article-content img::attr(src)').getall()


			yield(article)









