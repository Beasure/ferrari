# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ferrari.items import FerrariItem

class Ferrari488Spider(CrawlSpider):
    name = 'ferrari488'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/3720.html']

    rules = (
        Rule(LinkExtractor(allow=r"https://car.autohome.com.cn/pic/series/3720.+"),
             callback="parse_page", follow=True),
    )

    def parse_page(self, response):
        category = response.xpath("//div[@class='uibox']/div/text()").get()
        srcs = response.xpath("//div[contains(@class,'uibox-con')]/ul/li//img/@src").getall()
        srcs = list(map(lambda x: response.urljoin(x.replace("t_", "")), srcs))
        # srcs = list(map(lambda x: x.replace("t_", ""), srcs))
        # srcs = list(map(lambda x: response.urljoin(x), srcs))
        yield FerrariItem(category=category, image_urls=srcs)



    def test_page(self, response):
        uiboxs = response.xpath("//div[@class='uibox']")[1:]
        for uibox in uiboxs:
            category = uibox.xpath(".//div[@class='uibox-title']/a/text()").get()
            urls = uibox.xpath(".//ul/li/a/img/@src").getall()
            # for url in urls:
            #     url = response.urljoin(url)
            #     print(url)
            urls = list(map(lambda url: response.urljoin(url), urls))
            item = FerrariItem(category=category, image_urls=urls)
            yield item

