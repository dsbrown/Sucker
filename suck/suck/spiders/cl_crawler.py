# -*- coding: utf-8 -*-
import scrapy
import os
from suck.items import SuckItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

# Takes a string or list and returns a string the contents
def get_string(thing):
    out_str = ""

    if isinstance(thing, (int, long, float, complex,)):
        return(str(thing))

    for item in thing:
        if isinstance(item, str):
            out_str = out_str + item
        elif isinstance(item, list):
            out_str = out_str + get_string(item)
    return(out_str)

RootUrl =  "http://seattle.craigslist.org/"
class ClCrawlerSpider(CrawlSpider):
    name = "cl_crawler"
    allowed_domains = ["craigslist.org"]
    start_urls = [
        "http://seattle.craigslist.org/search/cto"
    ]
    
    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        #print "---------------------------------------------------"
        #print "Response Object: %s"%response.url
        titles = response.xpath("//span[@class='pl']")
        for title in titles:
            item = SuckItem()
            item['title'] = title.xpath('a/span[@id="titletextonly"]/text()').extract()
            item['time']  = title.xpath('time/@datetime').extract()
            #item['link'] = title.xpath('a/@href').extract()
            link = title.xpath('a/@href').extract()
            link = RootUrl+str(link[0])
            item['link'] = link
            item['key']  = title.xpath('a/@data-id').extract()           
            #print "---------------------------------------------------"
            #print "trying link: %s"%link
            new_request = Request(link, callback=self.parse_detail_page)
            new_request.meta['item'] = item
            yield new_request

    def parse_detail_page(self, response):
        item = response.meta['item']
        # <p class="attrgroup"> .... <span>cylinders:<b>6 cylinders</b></span> ... </p>
        #print "===================================================================="
        item['cylinders'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "cylinders")]').re(r'\<b\>(\d+\s.*)\<\/b\>')
        item['condition'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "condition")]').re(r'\<b\>(\w+)\<\/b\>')
        item['title_status'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "title status")]').re(r'\<b\>(\w+)\<\/b\>')
        item['transmission'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "transmission")]').re(r'\<b\>(\w+)\<\/b\>')
        item['v_type'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "type")]').re(r'\<b\>(\w+)\<\/b\>')
        item['size'] = response.selector.xpath('//p[@class="attrgroup"]/span[contains(., "size")]').re(r'\<b\>(\w+)\<\/b\>')
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
