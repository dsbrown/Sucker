# -*- coding: utf-8 -*-
import scrapy
import os
from suck.items import SuckItem

#        'http://seattle.craigslist.org/search/cto',
#  RSS feed looks like this: http://seattle.craigslist.org/search/cto?format=rss
# Pages http://seattle.craigslist.org/search/cto?s=0

class ClSpider(scrapy.Spider):
    name = "cl"
    allowed_domains = ["craigslist.org"]
    start_urls = [
        "http://seattle.craigslist.org/search/cto"
    ]

    # def parse(self, response):
    #     form = response.xpath('//body/section/form')
    #     filename = response.url.split("/")[-1]+".txt"
    #     with open(filename, 'w') as e:
    #         for p in form.xpath('.//a[@class="hdrlnk"]'):
    #             print "------------------------------------------------------------------"
    #             title = p.xpath('a/text()').extract()
    #             link = p.xpath('a/@href').extract()
    #             desc = p.xpath('text()').extract()
    #             print str(title), str(link), str(desc)
    #             print "------------------------------------------------------------------"

    #             out = p.extract()
    #             try:
    #                 out = str(out)
    #             except:
    #                 try:
    #                     out = out.encode("utf-8")
    #                 except:
    #                     out = out
    #             e.write(out)
    #             e.write(os.linesep)
    #             title = p.xpath('a/text()').extract()

    #     e.close


    def parse(self, response):
        titles = response.xpath("//span[@class='pl']")
        for title in titles:
            item = SuckItem()
            item['title'] = title.xpath('a/span[@id="titletextonly"]/text()').extract()
            item['time'] = title.xpath('time/@datetime').extract()         
            item['link'] = title.xpath('a/@href').extract()
            item['key'] = title.xpath('a/@data-id').extract()           
            yield item



        # print "------------------------------------------------------------------"
        # print "Title %s"%response.selector.xpath('//title/text()').extract()[0]
        # print form
        # print response.selector.xpath('//body/section/form/div')
        # for p in form.xpath('.//a'):
        #     print p.extract()
        # print "------------------------------------------------------------------"      
        
