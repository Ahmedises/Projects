# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WatchItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    price = scrapy.Field()
    reference_number = scrapy.Field()
    brand = scrapy.Field()
    series = scrapy.Field()
    movement = scrapy.Field()
    case_material = scrapy.Field()
    strap_material = scrapy.Field()
    gender = scrapy.Field()
    dial_color = scrapy.Field()
    glass = scrapy.Field()
    water_resistance = scrapy.Field()
    made_in = scrapy.Field()

