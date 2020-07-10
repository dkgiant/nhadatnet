import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ApartmentsSpider(CrawlSpider):
    name = 'apartments'
    allowed_domains = ['www.nhadat.net']
    start_urls = ['https://www.nhadat.net/ban-can-ho/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//div[@class="media-body media-middle"]/a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield{
            'title': response.xpath(r'//h1/text()').get(),
            'location': response.xpath(r'normalize-space(//div[@class="row Main_features"]/descendant::span[2]/text())').get(),
            'volume': response.xpath(r'normalize-space(//div[@class="row Main_features"]/descendant::span[6]/text())').get(),
            'legal': response.xpath(r'normalize-space(//div[@class="row Main_features"]/descendant::span[14]/text())').get(),
        }