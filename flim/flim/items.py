# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FlimItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    flim_name = scrapy.Field()
    flim_url = scrapy.Field()
    flim_info = scrapy.Field()
    flim_describe = scrapy.Field()
    flim_image = scrapy.Field()
    flim_image_url = scrapy.Field()
    flim_image_path = scrapy.Field()
    flim_image_name = scrapy.Field()
