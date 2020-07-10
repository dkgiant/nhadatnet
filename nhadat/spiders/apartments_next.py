import scrapy
import re


class ApartmentsNextSpider(scrapy.Spider):
    name = 'apartments_next'
    allowed_domains = ['www.nhadat.net']
    page = 1
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.nhadat.net/ban-can-ho?page=1', callback=self.parse, headers={
            'User-Agent': self.user_agent
        })

    def parse(self, response):
        apartments = response.xpath(
            r'//div[@class="media-body media-middle"]/a/@href').getall()
        for apart in apartments:
            url_apartment = response.urljoin(apart)
            yield scrapy.Request(url=url_apartment, callback=self.parse_item, headers={
                'User-Agent': self.user_agent
            })

        cur_page = response.xpath(
            r'(//ul[@class="pagination"])[1]/li[@class="active"]/a/@href').get()

        page_re = re.compile(r'(page=\d+)')

        self.page += 1
        next_page = page_re.sub('page=' + str(self.page), cur_page)

        url_next_page = response.urljoin(next_page)
        
        yield scrapy.Request(url=url_next_page, callback=self.parse, headers={
            'User-Agent': self.user_agent
        })

    def parse_item(self, response):
        yield{
            'title': response.xpath(r'//h1/text()').get(),
            'location': response.xpath(r'normalize-space(//div[@class="row Main_features"]/descendant::span[2]/text())').get(),
            'volume': response.xpath(r'normalize-space(//div[@class="row Main_features"]/descendant::span[6]/text())').get(),
            'legal': response.xpath(r'normalize-space(//div[@class="row Main_features"]/descendant::span[14]/text())').get(),
        }
