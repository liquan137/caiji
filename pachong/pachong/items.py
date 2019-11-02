# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time
from scrapy.pipelines.files import FilesPipeline

class MenuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pass

class ListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pass

class FileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    size = scrapy.Field()
    upload_time = scrapy.Field()
    create_time = scrapy.Field()
    file_type = scrapy.Field()
    color_type = scrapy.Field()
    down_png = scrapy.Field()
    pass
