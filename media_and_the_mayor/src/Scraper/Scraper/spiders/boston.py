# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from Scraper.items import Article



class BostonSpider(scrapy.Spider):
	name = 'boston'
	allowed_domains = ['www.boston.com', 'web.archive.org']
	start_urls = ['https://www.boston.com/']
	base_url = 'https://www.boston.com'

	visited, to_crawl = [], []
	years=['2014', '2015', '2016', '2017', '2018', '2019']


	def __init__(self, wayback=False, year='', *args, **kwargs):
		super(BostonSpider, self).__init__(*args, **kwargs)

		self.wayback = wayback
		self.year = year

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
		if not self.wayback or ('news' not in response.url and '/{}/'.format(any(year not in response.url for year in self.years))):
			self.visited.append(response.url)

		outgoing_links = response.css('a::attr(href)').getall()
		self.to_crawl += outgoing_links

		for url in self.to_crawl:
			self.to_crawl.remove(url)

			if url.startswith('/'):
				url = self.base_url + url

			main_site_url = 0

			if 'news' in response.url and any('/{}/'.format(year) in url for year in self.years) and '/news/' in response.url:
				main_site_url = url.split('boston.com')[-1]

			if url not in self.visited and main_site_url not in self.visited and self.is_valid(url):
				if any('/{}/'.format(year) in url for year in self.years):
					self.visited.append(main_site_url)

					yield SplashRequest(
						url = url, 
						callback = self.parse_article
					)

				print()
				print()
				print(url)
				print()
				print()

				yield scrapy.Request(
					url = url, 
					callback = self.parse
				)


	def parse_article(self, response):
		print()
		print()
		print('HI')
		print()
		print()
		article = Article()

		article['url'] = response.url

		article['journal'] = 'Boston.com'
		article['title'] = response.css('head title::text').get()
		article['summary'] = response.css('head meta[property="og:description"]::attr(content)').get()

		cand_body = response.css('body div.site-container div.content-text p::text').getall()

		if cand_body:
			article['tags'] = response.css('head meta[property="article:tag"]::attr(content)').getall()

			article['author'] = response.css('body div.content-byline__producer *::text').getall()

			article['date'] = response.css('head meta[property="article:published_time"]::attr(content)').get()

			article['body'] = cand_body

			article['media'] = response.css('body div.site-container article.content-well--article img::attr(src)').getall()
		
		elif response.css('body article.article-bd div.entry-txt p *::text'):
			article['tags'] = response.css('head meta[property="keywords:tag"]::attr(content)').getall()
			
			article['author'] = response.css('body article.article-bd li.story-byline a::text').get()
			
			article['date'] = response.css('head meta[name="publish-date"]::attr(content)').get()
			
			article['body'] = response.css('body article.article-bd div.entry-txt p *::text').get()
			
			article['media'] = response.css('body article.article-bd img::attr(src)').get()
		
		else:
			article['tags'] = response.css('head meta[property="keywords:tag"]::attr(content)').getall()

			article['author'] = response.css('body div#container div#content div.byline span.author::text').get()

			article['date'] = response.css('body div#container div#content div.byline span#dateline::text').getall()

			article['body'] = response.css('body div#container div#content section.article-text p::text').getall()

			article['media'] = response.css('body div#container div#content img::attr(src)').getall()


		if article['body']:
			yield article










