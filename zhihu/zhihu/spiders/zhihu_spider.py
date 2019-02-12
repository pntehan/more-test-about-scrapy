# -*- coding: utf-8 -*-
import scrapy
from zhihu.items import ZhihuItem

class ZhihuSpiderSpider(scrapy.Spider):
    name = 'zhihu_spider'
    allowed_domains = ['www.google.com']
    start_urls = ['https://www.google.com/search?q=%E6%96%8B%E8%97%A4%E9%A3%9E%E9%B8%9F&newwindow=1&safe=strict&source=lnms&tbm=isch&sa=X&ved=0ahUKEwioifv0qPffAhWLfLwKHcZ7DPoQ_AUIDigB&biw=1536&bih=754&gws_rd=cr']

    def parse(self, response):
        print(response.request.headers)
        print(response.request.meta)
        print(response.text)
        
