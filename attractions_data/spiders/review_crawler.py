from pathlib import Path
import re
import scrapy
import logging
import pandas as pd
from attractions_data.items import ReviewItems, ReviewItemLoader
from dotenv import load_dotenv
import os
from urllib.parse import urlencode

# Load environment variables from .env file
load_dotenv()


API_KEY = '6d69ef8259ea22a85451b0a00d790317'
SCRAPERAPI_PROXY = f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001'

class ReviewCrawler(scrapy.Spider):
    name = "reviews"
    allowed_domains = ['tripadvisor.ca']

    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'COOKIES_ENABLED': False,
        'AUTOTHROTTLE_ENABLED' : True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY' : 4,
        # 'USER_AGENT' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +https://www.google.com/bot.html)'
        # 'CONCURRECT_REQUESTS' : 4
    }

    headers = {
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.tripadvisor.ca/',
        }

    
    async def start(self):
        attraction_data = pd.read_json(r"U:\Travel_Recommendation_Project\attractions_data\attraction_list.json").iloc[316:,:]

        attraction_urls = attraction_data["attraction_url"].tolist()
        attraction_names = attraction_data["attraction_name"].tolist()

        for attraction_name,attraction_url in zip(attraction_names,attraction_urls):
            match = re.match(r'^(https://www\.tripadvisor\.ca/AttractionProductReview-g\d+-d\d+)-([A-Za-z_-]+\.html)$', attraction_url)
            if match:
                base_url = match.group(1)
                attraction_followup = match.group(2)
                yield scrapy.Request(url=attraction_url, 
                                    callback=self.parse_attraction_data, 
                                    cb_kwargs={'attraction_name': attraction_name}, 
                                    headers=self.headers,
                                    meta={'proxy': SCRAPERAPI_PROXY}
                                    )
                
            for idx in range(10,20,10):
                attraction_url = f"{base_url}-or{idx}-{attraction_followup}"
                
                yield scrapy.Request(url=attraction_url, 
                                    callback=self.parse_attraction_data, 
                                    cb_kwargs={'attraction_name': attraction_name},
                                    headers=self.headers,
                                    meta={'proxy': SCRAPERAPI_PROXY}
                                    )
    

    def parse_attraction_data(self, response,attraction_name):
        
        loader = ReviewItemLoader(item=ReviewItems(), response=response)
        
        location_details = response.css('div[data-automation="breadcrumbs"]')[0]
        location_details_items = location_details.css('div.buhZJ._T.Cj')
        
        country = location_details_items[0].xpath('.//div[contains(@class, "buhZJ _T")]/a/span/span/text()').get()
        province = location_details_items[1].xpath('.//div[contains(@class, "buhZJ _T")]/a/span/span/text()').get()
        city = location_details_items[4].xpath('.//div[contains(@class, "buhZJ _T")]/a/span/span/text()').get()

        
        # Optional attraction info - add only if available
        loader.add_value('attraction_name', attraction_name)
        loader.add_value('country', country)
        loader.add_value('province', province)
        loader.add_value('city', city)
        loader.add_xpath('price', './/div[contains(@class, "Cvebg")]/div[contains(@class, "biGQs")]/text()')
    
        # Review fields - multiple values expected
        loader.add_xpath('review_title', './/div[contains(@class, "biGQs _P")]/a/span/text()')
        loader.add_xpath('review_description', './/div[contains(@class, "_T FKffI")]/div/div/span/span/text()')
        loader.add_xpath('review_date', './/div[contains(@class, "TreSq")]/div[contains(text(), "Written")]/text()')
    
        yield loader.load_item()



# 18002091122
#     custom_settings = {
#     'AUTOTHROTTLE_ENABLED': True,
#     'AUTOTHROTTLE_START_DELAY': 5,
#     'AUTOTHROTTLE_MAX_DELAY': 15,
#     'CONCURRENT_REQUESTS_PER_DOMAIN': 2,
#     'ROBOTSTXT_OBEY': False,
#     'COOKIES_ENABLED': True
# }












#     headers = {
#     'authority': 'www.tripadvisor.ca',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'max-age=0',
#     'referer': 'https://www.google.com/',
#     'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'same-origin',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
# }






# jupyter bank  8655055086


















# travel_recommendation_system:
#     attraction_data:
#         attraction_data:
#            spyders:
#               attraction_crawler.py # working fine
#               review_crawler.py # here getting error.
#     venv
#     test.py
# meta={"playwright": True}

        # "User-Agent" : 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

        # 'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # HEADERS = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Connection": "keep-alive",
    #     "Upgrade-Insecure-Requests": "1",
    #     "Sec-Fetch-Dest": "document",
    #     "Sec-Fetch-Mode": "navigate",
    #     "Sec-Fetch-Site": "none",
    #     "Sec-Fetch-User": "?1",
    #     "Cache-Control": "max-age=0",
    # }

                    # payload = {'api_key': SECRET_KEY, 'url': attraction_url}
                
                # proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)

                                # payload = {'api_key': SECRET_KEY, 'url': attraction_url}
                # proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)


    # def parse_attraction_data(self, response, attraction_name):
    #     for review in response.css('div[data-automation="tab"]')[1:]:
    #         review_items = ReviewItems()
    #         review_items['attraction_name'] = attraction_name
    #         review_items['review_title'] = review.xpath('.//span[contains(@class, "yCeTE")]/text()').get()
    #         review_items['review_description'] = review.xpath('.//div[contains(@class, "_T FKffI")]/div/div/span/span/text()').get()
    #         review_items['review_date'] = review.xpath('.//div[contains(@class, "TreSq")]/div[contains(text(), "Written")]/text()').get()

    #         if review_items['review_title'] or review_items['review_description']:
    #             yield review_items


            # loader.add_xpath('country', './/div[contains(@class, "buhZJ _T")]/a/span/span/text()')
        # loader.add_xpath('province', '//span[@class="province"]/text()')
        # loader.add_xpath('city', '//span[@class="city"]/text()')
        # loader.add_xpath('location', '//div[@class="location"]/text()')
        # loader.add_xpath('price', '//span[@class="price"]/text()')