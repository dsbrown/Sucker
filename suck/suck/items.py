# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuckItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cl_main_title   = scrapy.Field()
    posting_time    = scrapy.Field()
    link            = scrapy.Field()
    key             = scrapy.Field()
    price           = scrapy.Field()    
    cylinders       = scrapy.Field()
    condition       = scrapy.Field()
    title_status    = scrapy.Field()
    transmission    = scrapy.Field()
    v_type          = scrapy.Field()
    v_size            = scrapy.Field()
    paint_color     = scrapy.Field()
    fuel            = scrapy.Field()
    drive           = scrapy.Field()
    odometer        = scrapy.Field()
    VIN             = scrapy.Field()
    map_longitude   = scrapy.Field()
    map_latitude    = scrapy.Field()
    map_accuracy    = scrapy.Field()
    map_link        = scrapy.Field()
    address         = scrapy.Field()
    content         = scrapy.Field()    
    detail_title    = scrapy.Field()    
    image_urls      = scrapy.Field()
    images          = scrapy.Field()



