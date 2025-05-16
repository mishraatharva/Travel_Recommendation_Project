# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
# from scrapy.processors import TakeFirst, MapCompose
from itemloaders.processors import TakeFirst,MapCompose


class AttractionsDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ReviewItems(scrapy.Item):
    attraction_name = scrapy.Field()
    country = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    price = scrapy.Field()
    
    review_title = scrapy.Field()
    review_description = scrapy.Field()
    review_date = scrapy.Field()


def replace_empty_with_na(value):
    if not value or value.strip() == '':
        return 'na'
    return value.strip()

class ReviewItemLoader(ItemLoader):
    # For attraction info, get first value or None (optional)
    attraction_name_out = TakeFirst()
    country_out = TakeFirst()
    province_out = TakeFirst()
    city_out = TakeFirst()
    price_out = TakeFirst()
    
    # For review fields, process each value to replace empty with 'na', keep as list
    review_title_out = MapCompose(replace_empty_with_na)
    review_description_out = MapCompose(replace_empty_with_na)
    review_date_out = MapCompose(replace_empty_with_na)
