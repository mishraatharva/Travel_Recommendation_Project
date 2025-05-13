from pathlib import Path
import re
import scrapy
import logging

class AttractionCrawler(scrapy.Spider):
    name = 'attraction_crawler'
    allowed_domains = ['tripadvisor.ca']
    start_urls = ['https://www.tripadvisor.ca/Attraction_Products-g153339-Canada.html']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False
    }

    def parse(self, response):
        # Loop over each attraction card/section
        for card in response.css('div[data-automation="cardWrapper"]'):
            url = card.css('a[href*="AttractionProductReview"]::attr(href)').get()
            if url:
                absolute_url = response.urljoin(url)
            else:
                continue
            
            name_parts = card.xpath('.//div[contains(@class, "XfVdV")]/span/text() | .//div[contains(@class, "XfVdV")]/text()').getall()
            
            avg_rating = card.css('div[data-automation="bubbleRatingValue"]::text').get()
            total_person_rated = card.css('div[data-automation="bubbleLabel"]::text').get()
            
            numbered_name = ''.join(name_parts).strip()
            
            yield {
                "attraction_name": numbered_name,
                "avg_rating" : avg_rating,
                "total_person_rated": total_person_rated,
                'attraction_url': absolute_url
            }
        
        pagination_section = response.css('section[data-automation="WebPresentation_PaginationLinksList"]')
        next_page = pagination_section.css('a[aria-label="Next page"]::attr(href)').get()
        
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"Following next page: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("No next page found, crawling finished.")