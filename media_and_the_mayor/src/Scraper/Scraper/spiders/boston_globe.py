# -*- coding: utf-8 -*-
import scrapy

from Scraper.items import Article

from datetime import datetime



class BostonGlobeSpider(scrapy.Spider):
	name = 'boston_globe'
	allowed_domains = ['www.bostonglobe.com', 'web.archive.org']
	start_urls = ['https://www.bostonglobe.com/']
	base_url = 'https://www.bostonglobe.com'

	visited, to_crawl = [], []
	

	def __init__(self, wayback=False, year='', *args, **kwargs):
		super(BostonGlobeSpider, self).__init__(*args, **kwargs)

		self.wayback = wayback

		if wayback:
			self.base_url = 'http://web.archive.org'
			with open('./Wayback/{}{}.csv'.format(self.name, year), 'r') as f:
				self.start_urls = [cached_version.strip('\n') for cached_version in f.readlines()[1:]]


	def start_request(self):
		for url in self.start_urls:
			yield scrapy.Request(
				url = url, 
				callback = self.parse
			)


	def is_valid(self, url):
		if self.allowed_domains[0] in url:
			return True

		return False


	def parse(self, response):
		if not self.wayback or 'story.html' not in response.url:
			self.visited.append(response.url)

		outgoing_links = response.css('a::attr(href)').getall()
		self.to_crawl += outgoing_links

		for url in self.to_crawl:
			self.to_crawl.remove(url)

			if url.startswith('/'):
				url = self.base_url + url

			boston_globe_url = 0

			if 'story.html' in url:
				boston_globe_url = url.split('bostonglobe.com')[-1]

			if url not in self.visited and boston_globe_url not in self.visited and self.is_valid(url):
				if 'story.html' in url:
					self.visited.append(boston_globe_url)

					yield scrapy.Request(
						url = url, 
						callback = self.parse_article
					)

				yield scrapy.Request(
					url = url, 
					callback = self.parse
				)


	def parse_article(self, response):
		outgoing_links = response.css('a::attr(href)').getall()
		
		for url in outgoing_links:
			if url.startswith('/'):
				url = self.base_url + url

			if url not in self.visited and self.is_valid(url):
				self.to_crawl.append(url)


		article = Article()


		article['url'] = response.url
		
		article['journal'] = 'Boston Globe'
		
		article['title'] = response.css('head title::text').get().replace(' - The Boston Globe', '')
		
		article['tags'] = response.css('head meta[name=keywords]::attr(content)').get()

		article['summary'] = response.css('head meta[name=description]::attr(content)').get()

		article['body'] = None


		if response.css('div#fusion-app section#article-right-rail div.article'):
			'''
				2019
			'''
			
			article['author'] = response.css('div#header-container div.article div.byline div.authors span.author span.bold:not(.seperator)::text').getall()
			
			article['date'] = response.css('div#header-container div.article div.byline span.datetime span.date::text').get()
			
			article['body'] = ' '.join(response.css('div#fusion-app section#article-right-rail div.article p.paragraph span::text').getall())

			article['media'] = response.css('div.fusion-app article img::attr(src)').getall()

		elif response.css('body div.article-body div.article-content').get():
			'''
				late 2017, 2018
			'''
			
			article['author'] = response.css('body span.article-header__byline-author a span::text').getall()
			
			article['date'] = response.css('body div.article-body time::text').get()
			
			article['body'] = ' '.join(response.css('body div.article-content p::text').getall())

			article['media'] = response.css('body div.article-body img::attr(src)').getall()

		elif response.css('body div.article-body div.article-text'):
			'''
				2015, 2016, early 2017
			'''

			article['author'] = response.css('body div.byline b.author *::text').getall()
			
			article['date'] = response.css('body div.article-body time::text').get()
			
			article['body'] = ' '.join(response.css('body div.article-text p::text').getall())

			article['media'] = response.css('body div.article-body img::attr(src)').getall()

		elif response.css('body div.article-body content'):
			'''
				2014
			'''
			article['author'] = response.css('body h2.author *::text').getall()
			
			article['date'] = 2014

			article['body'] = ' '.join(response.css('body div.article-body content p::text').getall())

			article['media'] = response.css('body div.article-body img::attr(src)').getall()

		
		if article['body']:
			yield article
		else:
			self.to_crawl.append(response.url)






