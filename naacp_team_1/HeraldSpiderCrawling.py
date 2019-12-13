from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from pymongo import MongoClient
import re


def getTags(s):
    
    # NOTE: THIS IS NOT AN EXHAUSTIVE LIST OF GEOGRAPHIES IN BOSTON
    neighborhoods = ['Allston', 'Brighton', 'Back Bay', 'North End', 'Roxbury',
                     'Bay Village', 'Beacon Hill', 'Charlestown', 'Chinatown',
                     'Dorchester', 'Downtown', 'East Boston', 'Kenmore', 'Fenway',
                     'Hyde Park', 'Jamaica Plain', 'Mattapan', 'Mission Hill',
                     'Roslindale', 'South Boston', 'South End', 'West End', 
                     'West Roxbury', ]   
    
    tags = []
    
    for neighborhood in neighborhoods:
        if bool(re.search(neighborhood, s)):
            tags.append(neighborhood)
    
    return tags


class MongoDB:
    """
    we need to create a single persistent connection to database.

    Everytime a client calls us, we can simply return the connection instead of creating
    it again and again.
    """
    def __init__(self):
        self.db = MongoClient("mongodb://localhost:3000/")

    def get_database(self):
        return self.db

    def get_client(self, db_name):
        return self.db[db_name]


class HeraldSpiderCrawler(CrawlSpider):
    name = 'heraldcrawler_update'

    db_client = MongoDB()

    allowed_domains = ["bostonherald.com"]
    start_urls = ['https://www.bostonherald.com/news/local-news', 'http://www.bostonherald.com/news_opinion/local_coverage', 'http://www.bostonherald.com/news/local_coverage']

    custom_settings = {
        'DEPTH_LIMIT': 2
    }
    rules = (
        Rule(LinkExtractor(allow = (), restrict_xpaths = (['//h4[@class="entry-title"]',
                                                           '//span[@class="sub-section"]/h1',
                                                           '//h2[@class="node-title"]'])),
        callback="parse_items",
        follow=True),
    )

    def parse_items(self, response):
        items = []
        tags = []

        for paragraph in response.xpath('//div[@class="body-copy"]/p'):
            try:
                text = paragraph.xpath('text()').getall()
                items.append(text)
            except:
                pass
            
        for paragraph in response.xpath('//div[@class="content-body"]/p'):
            try:
                text = paragraph.xpath('text()').getall()
                items.append(text)
            except:
                pass    

        for paragraph in response.xpath('//div[@class="field-item"]/p'):
            try:
                text = paragraph.xpath('text()').getall()
                items.append(text)
            except:
                pass
        
        for paragraph in response.xpath('//div[@class="field-items"]//p'):
            try:
                text = paragraph.xpath('text()').getall()
                items.append(text)
            except:
                pass

        # tag and clean the story
        flat_items = [item for sublist in items for item in sublist]
        story = " ".join(flat_items)
        story = story.replace('\n\t ','')
        story = story.replace('\t ','')
        story = story.replace('\n ','')
        
        
        tags = getTags(story)
        
        story = story.lower()

        if len(items) > 0:

            db = self.db_client.get_client(self.db_name)
            timestamp = response.meta['wayback_machine_time'].timestamp()

            master_collection = db[self.collection_name]
            document = {'timestamp': timestamp, 'story': story}
            
            count = master_collection.count_documents({'story': {'$in': [story]}})
            # primitive duplicate handling
            if count == 0:
                
                # always insert into master
                master_collection.insert_one(document)
                for tag in tags:
                    collection_by_tag = db[tag.lower().replace(" ", "_")]
                    collection_by_tag.insert_one(document)
            return document
