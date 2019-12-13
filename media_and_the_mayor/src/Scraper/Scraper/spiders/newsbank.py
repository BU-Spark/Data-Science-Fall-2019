# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from scrapy_splash import SplashRequest, SplashFormRequest

from Scraper.items import Article



class NewsbankSpider(scrapy.Spider):
    name = 'newsbank'
    #allowed_domains = ["https://infoweb-newsbank-com.ezproxy.bu.edu"]
    base_url = 'https://infoweb-newsbank-com.ezproxy.bu.edu'
    
    # All Boston journals
    start_url = base_url + '/apps/news/browse-multi?p=AWNB&t=custom%3ACustBucket1%21Boston%2520Metropolitan%2520Collection&action=browse'
    # Specific journals
    newspapers = [
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ABNHB!Boston%2BHerald%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AZBAB!Allston-Brighton%2BTAB%2B%2528Needham%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ABOBH!Boston%2BMagazine%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ADRDD!Dorchester%2BReporter%252C%2BThe%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ABCTH!Heights%252C%2BThe%253A%2BBoston%2BCollege%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AJPGB!Jamaica%2BPlain%2BGazette%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AMMBON!Mass%2BMedia%252C%2BThe%253A%2BUniversity%2Bof%2BMassachusetts%2B-%2BBoston%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AMRBB!Metro%2B-%2BBoston%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AMHGB!Mission%2BHill%2BGazette%2B%2528Jamaica%2BPlain%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AMNBP!NewBostonPost%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AZBCK!Roslindale%2BTranscript%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ASVMA!Simmons%2BVoice%252C%2BThe%253A%2BSimmons%2BCollege%2B%2528Boston%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ASENB!South%2BEnd%2BNews%2B%2528Boston%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ASJB1!Suffolk%2BJournal%252C%2BThe%253A%2BSuffolk%2BUniversity%2B%2528Boston%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3ASVSUB!Suffolk%2BVoice%252C%2BThe%253A%2BSuffolk%2BUniversity%2B%2528Boston%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AUHBB!Universal%2BHub%2B%2528Boston%252C%2BMA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AZBDF!West%2BRoxbury%2BTranscript%2B%2528MA%2529&action=browse', 
        '/apps/news/browse-pub?p=AWNB&t=pubname%3AAPM89!Associated%2BPress%253A%2BBoston%2BMetro%2BArea%2B%2528MA%2529&action=browse'
    ]


    # Pass your BU credentials
    #username = input('BU Username: ')
    #password = input('BU Password: ')

    # Login and start the session
    # We have to have enough wait time for all the redirections to take place, 
    # but this is only for the first request. 
    lua_login = '''
        function main(splash)
            splash:init_cookies(splash.args.cookies)
            assert(splash:go(splash.args.url))
            assert(splash:wait(10))
            splash:set_viewport_full()
            
            local form = splash:select('form')
            assert(form:fill({
                user=splash.args.username, 
                pw2=splash.args.password, 
                pw=splash.args.password
            }))
            assert(form:submit())
            assert(splash:wait(10))
            
            return{
                cookies = splash:get_cookies(), 
                html = splash:html()
            }
        end
    '''

    # Use session in every request
    lua_cookies = '''
        function main(splash)
            splash:init_cookies(splash.args.cookies)
            assert(splash:go(splash.args.url))
            splash:set_viewport_full()
            
            return{
                cookies = splash:get_cookies(), 
                html = splash:html()
            }
        end
    '''

    articles = []

    
    def start_requests(self):
        '''
            The first request is used to create the session. 
            Must be done even if it's a dummy one
        '''
        print('\n LOGGING IN \n')

        yield SplashRequest(
            url = self.start_url,
            callback = self.parse_newspapers, 
            cache_args = ['lua_source'], 
            endpoint = 'execute', 
            args = {
                'username' : self.username, 
                'password' : self.password, 
                'lua_source' : self.lua_login
            }
        )


    def parse_newspapers(self, response):
        '''
            Go to the main page of a specific newspaper
        '''
        print('\n PARSING NEWSPAPERS \n')

        for newspaper_url in self.newspapers:
            yield SplashRequest(
                url = self.base_url + newspaper_url,
                callback = self.get_date, 
                cache_args = ['lua_source'], 
                endpoint = 'execute', 
                args = {
                    'lua_source' : self.lua_cookies
                }
            )


    def get_year(self, response):
        print('\n  \n')

        script = '''
            function main(splash)
                splash:init_cookies(splash.args.cookies)
                assert(splash:go(splash.args.url))
                splash:set_viewport_full()
                assert(splash:wait(10))

                splash:runjs("document.querySelector('select option[value=splash.args.year_select]').selected = 'true';")

                assert(splash:wait(10))
                
                return{
                    cookies = splash:get_cookies(), 
                    html = splash:html()
                }
            end
        '''

        years = ['2014']
        
        for year in years:
            yield SplashRequest(
                url = response.url, 
                callback = self.get_date, 
                cache_args = ['lua_source'], 
                endpoint = 'execute', 
                args = {
                    'year_select' : year, 
                    'js_source' : "document.querySelector('select option[value='2014']').selected = 'true';", 
                    'lua_source' : self.lua_cookies
                }
            )

        
    def get_date(self, response):
        '''
            Get get the link to the latest posts
            of a specific url
        '''
        print('\n EXTRACTING DATES \n')

        # get the date of the latest publications
        year_articles = response.css('div.browsepub__calendar a::attr(href)').getall()

        for day_articles in year_articles:
            yield SplashRequest(
                url = self.base_url + day_articles, 
                callback = self.get_articles_by_date, 
                endpoint = 'execute', 
                args = {
                    'lua_source' : self.lua_cookies
                }
            )


    def get_articles_by_date(self, response):
        '''
            Go to the link of publications
            for a specific day for a specific newspaper
        '''
        print('\n EXTRACTING ARTICLES BY DATE \n')

        #  get articles' urls
        self.articles.extend(response.css('div.toc__wrapper a::attr(href)').getall())

        for article_url in self.articles:
            yield SplashRequest(
                url = self.base_url + article_url, 
                callback = self.scrape_article, 
                endpoint = 'execute', 
                args = {
                    'lua_source' : self.lua_cookies
                }
            )


    def scrape_article(self, response):
        '''
            Scrape a given article
        '''
        print('\n PARSING ARTICLE \n')
        new_article = Article()

        try:
            new_article['url'] = response.url
        except:
            new_article['url'] = None

        try:
            new_article['title'] = response.css('h1.document-view__title::text').get()
        except:
            new_article['title'] = None
        
        try:
            new_article['date'] = response.css('span.display-date::text').get()
        except:
            new_article['date'] = None
        
        try:
            new_article['journal'] = response.css('span.source::text').get().replace('\n', '')
        except:
            new_article['journal'] = None
        
        try:
            new_article['category'] = response.css('span.section::text').get().split(': ')[-1]
        except:
            new_article['category'] = None
        
        try:
            new_article['page_number'] = response.css('span.page::text').get().split(': ')[-1]
        except:
            new_article['page_number'] = None
        
        try:
            body = response.css('div.document-view__body p::text').getall()

            if body[-1].startswith('-- '):
                new_article['source'] = body[-1].replace('-- ', '')
                new_article['body'] = ' '.join(body[:-1])
            else:
                new_article['body'] = ' '.join(body)
        except:
            new_article['body'] = None
        

        yield new_article






