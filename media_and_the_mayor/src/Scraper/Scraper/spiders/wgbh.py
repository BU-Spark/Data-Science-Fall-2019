# -*- coding: utf-8 -*-
import scrapy

from Scraper.items import Article



class WgbhSpider(scrapy.Spider):
	name = 'wgbh'
	allowed_domains = ['www.wgbh.org']
	start_urls = [
		'https://www.wgbh.org/news/local-news', 
		'https://www.wgbh.org/news/politics', 
		'https://www.wgbh.org/news/education', 
		'https://www.wgbh.org/news/science-and-technology', 
		'https://www.wgbh.org/news/commentary'
	]


	def __init__(self, start_year=0, *args, **kwargs):
		super(WgbhSpider, self).__init__(*args, **kwargs)

		self.start_year = int(start_year)


	def parse(self, response):
		next_page = response.css('a.LoadMore-link::attr(href)').get()

		articles = response.css('div#main-content main#Page-main ul.FourUp-items li a::attr(href)').getall()
		date = response.css('div.PromoNews-date::text').get()

		try:
			curr_year = int(date.split(' ')[2])
		except:
			curr_year = 2019

		if curr_year >= self.start_year: 
			for article_url in articles:
				yield scrapy.Request(
					url = article_url, 
					callback = self.parse_article
				)

		if next_page:
			yield scrapy.Request(
				url = response.url.split('?')[0] + next_page, 
				callback = self.parse
			)


	def parse_article(self, response):
		article = Article()


		article['url'] = response.url
		
		article['journal'] = 'WGBH'
		
		article['date'] = response.css('span.ArticlePage-datePublished::text').get()
		
		article['author'] = response.css('div.ArticlePage-authorName a::text').getall()
		
		article['title'] = response.css('head title::text').get()
		
		article['category'] = response.css('head meta[property="article:section"]::attr(content)').get()
		
		article['summary'] = response.css('head meta[name="description"]::attr(content)').get()
		
		article['body'] = ' '.join(response.css('div.RichTextArticleBody-body p::text').getall())
		
		article['media'] = response.css('head meta[property="og:image"]::attr(content)').getall()


		yield article

