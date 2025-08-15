# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    Movie = scrapy.Field()
    Directors = scrapy.Field()
    Writers = scrapy.Field()
    Stars = scrapy.Field()
    Link = scrapy.Field()
    Rating = scrapy.Field()
    Meta_score = scrapy.Field()
    Tags = scrapy.Field()
    Preview = scrapy.Field()
    Year = scrapy.Field()
    # Image = scrapy.Field()

