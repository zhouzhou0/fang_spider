# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewhouseItem(scrapy.Item):
    city=scrapy.Field()
    origin_url = scrapy.Field()
    price = scrapy.Field()
    state = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    rooms = scrapy.Field()
    cell_name = scrapy.Field()
    province = scrapy.Field()

class EsfhouseItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    cell_name = scrapy.Field()
    address = scrapy.Field()
    rooms = scrapy.Field()
    floor=scrapy.Field()
    toward=scrapy.Field()
    year=scrapy.Field()
    area=scrapy.Field()
    price=scrapy.Field()
    unit=scrapy.Field()
    origin_url = scrapy.Field()


