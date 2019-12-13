from datetime import datetime as dt
import scrapy
from requests_html import HTMLSession
from retrying import retry

class GlobeSpider(scrapy.Spider):
    name = 'globe'

    @retry(stop_max_attempt_number=100, wait_fixed=10000)
    def start_requests(self):
        f = open("wgbh.txt")
        line = f.readline()
        while(line):
            session = HTMLSession()
            url = line

            try:
                r = session.get(url)
            except:
                continue
            for link in r.html.absolute_links:
                #if '/metro/' in link or '/sports/' in link or '/business/' in link or '/politics/' in link or '/opinion/' in link or '/lifestyle/' in link or '/arts/' in link:
                yield scrapy.Request(link)
            line = f.readline()

    def parse(self, response):
        items = []

       # for trend in response.xpath('//div[@class="article-content"]/p') or response.xpath('//div[@class="article-text"]/p') or response.xpath('//li[@class="listing-description"]/p') or response.xpath('//div[@class="article-body"]/content/p'):
        for trend in response.xpath('//div[@itemprop="articleBody"]/p')or response.xpath('//div[@class="abody clearfix"]/p')or response.xpath('//div[@class="article-content generic-txt "]/p')or response.xpath('//div[@class="post article"]/p')or response.xpath('//section[@class="article-section--content hang-punctuation article-section--first article-section--centered"]/p')or response.xpath('//div[@class="field-item even"]/p'):
            try:
                topic = trend.xpath('text()').getall()
                items.append(topic)
            except:
                pass
            '''


'''
        if len(items) > 0:

            return {'text':items}

# scrapy runspider globeSpider.py -o trends.json