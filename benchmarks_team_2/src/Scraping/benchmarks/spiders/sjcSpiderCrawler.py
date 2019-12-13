import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule 
from scrapy.linkextractors import LinkExtractor
# from benchmarks.benchmarks.items import BenchmarksItem
from items import BenchmarksItem
from collections import defaultdict
from pymongo import MongoClient 
import csv 
class SJCSpiderCrawler(CrawlSpider):
    name = 'sjccrawler'

    # adding an instance of our 
    # db_client = MongoDB()
    # where to start scrapings
    # only accept certain links to traverse through 
    # only want to go through sjc opinion text
    allowed_domains = ['masscases.com']
    # going to read in the file 
    download_delay = 5

    file = open('C:/Users/tiamm/Desktop/benchmarks/benchmarks/benchmarks/urls/urls.csv')
    start_urls = [line.strip() for line in file]

    
    # tells scrapy which function to use when parsing the Response 
    # object it get back after requesting the content of the links it 
    # finds insider the xpath we give it
    custom_settings = {
        'DEPTH_LIMIT': 5,
        'Download_DELAY': 5
    }

    rules = (
        Rule(LinkExtractor(allow=(),restrict_xpaths = ('//tr/td/a')) ,
        callback = 'parse_items',follow=True),
    )
    
    def extract_data(self,response,type):
        ''' type either needs to be 'case','headnote', or 
            'text'
        '''
        if type == 'case':
            data_ = response.xpath('////header[@class="w3-container"]/h1/text()').extract()
        elif type == 'headnote':
            response.xpath('//secton[@class="headnote"]/p/text()').extract()
        else:
            data_ = response.xpath('//secton[@class="opinion"]/p/text()').extract()
        data_ = [value.lstrip().rstrip() for value in data_]
        return data_
    
    def parse_cases(self,response):
        # getting the title, headnote, and opinion of the 
        # case, also going to preprocess the 
        item = BenchmarksItem(
            case=self.extract_data(response,'case'),
            headnote=self.extract_data(response,'headnote'),
            text=self.extract_data(response,'text'))
        yield item 