# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AttractionsDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ReviewItems(scrapy.Item):
    attraction_name = scrapy.Field()
    review_title = scrapy.Field()
    review_description = scrapy.Field()