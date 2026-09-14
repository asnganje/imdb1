# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy

class MovieItem(scrapy.Item):
    name = scrapy.Field()
    director = scrapy.Field()
    year = scrapy.Field()
    duration = scrapy.Field()
    stars = scrapy.Field()
    votes = scrapy.Field()
    metascore = scrapy.Field()
    description = scrapy.Field()
