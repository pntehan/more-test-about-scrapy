# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/top250']

    def parse(self, response):
        # print(response.request.headers['User-Agent'])
        # print(response.request.meta['pxory'])
        content = response.xpath("//*[@id='content']/div[1]/div[1]/div[1]/table/tr")
        if content:
            for book in content:
                book_link = book.xpath("./td[1]/a/@href").extract_first()
                yield scrapy.Request(book_link, callback=self.get_data)
        next_link = response.xpath("//*[@id='content']/div/div[1]/div/div/span[3]/a/@href").extract_first()
        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)
                
    def get_data(self, response):
        book = DoubanItem()
        book['book_name'] = response.xpath("//*[@id='wrapper']/h1/span/text()").extract_first()
        book['book_image_url'] = response.xpath("//*[@id='mainpic']/a/@href").extract_first()
        info = response.xpath("//*[@id='info']")
        for one in info:
            book['book_info'] = "".join(one.xpath("string(.)").extract_first().split())
        describe = response.xpath("//*[@id='link-report']/div[1]/div")
        if not describe:
            describe = response.xpath("//*[@id='link-report']/span[2]/div/div")
        for two in describe:
            book['book_describe'] = "".join(two.xpath("string(.)").extract_first().split())
        book['book_star'] = '豆瓣评分:'+response.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()").extract_first()
        yield book