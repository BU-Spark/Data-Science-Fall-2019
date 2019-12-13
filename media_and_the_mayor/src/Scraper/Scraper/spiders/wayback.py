# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from Scraper.items import WaybackDates

import time


class WaybackSpider(scrapy.Spider):
	name = 'wayback'
	allowed_domains = ['http://web.archive.org']

	load_calendar = '''
		function main(splash)
			assert(splash:go(splash.args.url))

			while not splash:select(splash.args.element) do
				splash:wait(0.1)
			end
			return {html=splash:html()}
			end
	'''


	def __init__(self, base_url, start_year=None, final_year=None, *args, **kwargs):
		super(WaybackSpider, self).__init__(*args, **kwargs)

		if not start_year:
			start_year = 1980

		if not final_year:
			final_year = 2019

		start_year = int(start_year)
		final_year = int(final_year)

		for year in range(start_year, final_year + 1, 1):
			self.start_urls.append('http://web.archive.org/web/{}0101000000*/{}'.format(str(year), base_url))


	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(
				url = url, 
				callback = self.parse, 
				endpoint='execute', 
				args = {
					'element' : 'div.calendar-day a', 
					'lua_source' : self.load_calendar
				}
			)


	def parse(self, response):
		cached_versions = WaybackDates()

		year_dates = [self.allowed_domains[0] + element for element in response.css('div.calendar-day a::attr(href)').getall()]

		for date in year_dates:
			cached_versions['date'] = date
			
			yield cached_versions







