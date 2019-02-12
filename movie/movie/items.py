# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_describe = scrapy.Field()
    movie_name = scrapy.Field()
    movie_url = scrapy.Field()
    movie_image = scrapy.Field()
    movie_image_path = scrapy.Field()
