# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['music.douban.com']
    start_urls = ['https://music.douban.com/top250']

    def parse(self, response):
        # print(response.request.headers['User-Agent'])
        # print(response.request.meta['pxory'])
        content = response.xpath("//*[@id='content']/div[1]/div[1]/div[1]/table/tr")
        if content:
            for music in content:
                music_link = music.xpath("./td[1]/a/@href").extract_first()
                yield scrapy.Request(music_link, callback=self.get_data)
        next_link = response.xpath("//*[@id='content']/div/div[1]/div/div/span[3]/a/@href").extract_first()
        if next_link:
            yield scrapy.Request(next_link, callback=self.parse)
                
    def get_data(self, response):
        music = DoubanItem()
        print('------------------------')
        music['music_name'] = response.xpath("//*[@id='wrapper']/h1/span/text()").extract_first()
        content = response.xpath("//*[@id='content']/div/div[1]")
        if content:
            music['music_image_url'] = content.xpath("//*[@id='mainpic']/span/a/@href").extract_first()
            info = content.xpath("//*[@id='info']")
            for one in info:
                music['music_info'] = "".join(one.xpath("string(.)").extract_first().split())
            music['music_describe'] = response.xpath("//*[@id='link-report']/span[2]/text()").extract_first()
        music['music_star'] = '豆瓣评分:'+response.xpath("//*[@id='interest_sectl']/div/div[2]/strong/text()").extract_first()
        yield music