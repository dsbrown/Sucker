from scrapy.spiders import BaseSpider

class ClSpider(BaseSpider):
    name = "cl"
    allowed_domains = ["craigslist.org"]
    start_urls = [
        "https://seattle.craigslist.org/search/see/cto",
    ]

    def parse(self, response):
    	print "------------------------------------------------------------------"
    	print "Title %s"%response.selector.xpath('//title/text()').extract()[0]
    	print "------------------------------------------------------------------"    	
        filename = response.url.split("/")[-1]+".html"
        open(filename, 'wb').write(response.body)
