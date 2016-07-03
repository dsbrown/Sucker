# -*- coding: utf-8 -*-
import scrapy
import os
from suck.items import SuckItem

#        'http://seattle.craigslist.org/search/cto',
#  RSS feed looks like this: http://seattle.craigslist.org/search/cto?format=rss
# Pages http://seattle.craigslist.org/search/cto?s=0
#
# Be sure to set ROBOTSTXT_OBEY = False to download images
#

class ClDetailSpider(scrapy.Spider):
    name = "cl_detail"
    allowed_domains = ["craigslist.org"]
    start_urls = [
        "http://seattle.craigslist.org/see/cto/5619319264.html",
        "http://seattle.craigslist.org/oly/cto/5653294384.html",
        "http://seattle.craigslist.org/see/cto/5622291929.html",
        "http://seattle.craigslist.org/see/cto/5637749678.html",
        ]
   
    def parse(self, response):
        item = SuckItem()
        item['cylinders'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "cylinders")]').re(r'\<b\>(\d+\s.*)\<\/b\>')
        item['condition'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "condition")]').re(r'\<b\>(\w+)\<\/b\>')
        item['title_status'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "title status")]').re(r'\<b\>(\w+)\<\/b\>')
        item['transmission'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "transmission")]').re(r'\<b\>(\w+)\<\/b\>')
        item['v_type'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "type")]').re(r'\<b\>(\w+)\<\/b\>')
        item['v_size'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "size")]').re(r'\<b\>(\w+)\<\/b\>')
        item['paint_color'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "paint color")]').re(r'\<b\>(\w+)\<\/b\>')
        item['fuel'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "fuel")]').re(r'\<b\>(\w+)\<\/b\>')
        item['drive'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "drive")]').re(r'\<b\>(\w+)\<\/b\>')
        item['odometer'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "odometer")]').re(r'\<b\>(\w+)\<\/b\>')
        item['VIN'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "VIN")]').re(r'\<b\>(\w+)\<\/b\>')

        #<div id="map" class="viewposting leaflet-container leaflet-fade-anim" data-accuracy="22" data-longitude="-122.548800" data-latitude="47.764807" tabindex="0">
        t = response.selector.xpath('//div[@class="mapbox"]/div[@id="map"]')
        item['map_longitude']= t.xpath("@data-longitude").extract()
        item['map_latitude'] = t.xpath("@data-latitude").extract()
        item['map_accuracy'] = t.xpath("@data-accuracy").extract()
        item['map_link'] = response.selector.xpath('//div[@class="mapbox"]/p[@class="mapaddress"]/small/a/@href').extract() 
        # <div class="mapaddress">2741 SE Arcadia Rd</div>
        item['address'] = response.selector.xpath('//div[@class="mapbox"]/div[@class="mapaddress"]/text()').extract()
        #<span class="price">$30000</span>
        item['price']  = response.selector.xpath('//span[@class="price"]/text()').extract()
        # <head>/<title>1981 El Camino</title>
        item['detail_title'] = response.selector.xpath('//head/title/text()').extract()
        #<section id="pagecontainer">/<section class="body">/<section class="userbody">/<section id="postingbody">
        item['content'] =  response.selector.xpath('//section[@id="pagecontainer"]/section[@class="body"]/section[@class="userbody"]/section[@id="postingbody"]/text()').extract()
        image_url = response.selector.xpath('//head/meta[@property="og:image"]/@content').extract()
        #print "Image: %s"%image_url
        item['image_urls'] = image_url

        yield item



