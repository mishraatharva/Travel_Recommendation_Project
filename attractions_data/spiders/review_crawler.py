from pathlib import Path
import re
import scrapy
import logging
import pandas as pd
from attractions_data.items import ReviewItems

class ReviewCrawler(scrapy.Spider):
    name = "reviews"
    allowed_domains = ['tripadvisor.ca']

    review_items = ReviewItems()

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False
    }

    async def start(self):
        urls = pd.read_json(r"U:\Travel_Recommendation_Project\attractions_data\attraction.json")["attraction_url"].tolist()
        attraction_names = pd.read_json(r"U:\Travel_Recommendation_Project\attractions_data\attraction.json")["attraction_name"].tolist()

        for attraction_name,attraction_url in zip(attraction_names,urls):
            yield scrapy.Request(url=attraction_url, callback=self.parse, cb_kwargs={'attraction_name': attraction_name})
    
    def parse(self, response, attraction_name):
        for review in response.css('div[data-automation="tab"]')[1:]:
            review_items = ReviewItems()
            first_page = True
            if first_page:
                review_items['attraction_name'] = attraction_name
                review_items['review_title'] = review.xpath('.//span[contains(@class, "yCeTE")]/text()').get()
                review_items['review_description'] = review.xpath('.//div[contains(@class, "_T FKffI")]/div/div/span/span/text()').get()
                yield review_items
                first_page = False
            