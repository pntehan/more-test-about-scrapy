# -*- coding: utf-8 -*-
import scrapy
from urllib import request
import urllib
import re
from baidu.items import BaiduItem

class BaiduSpiderSpider(scrapy.Spider):
    name = 'baidu_spider'
    allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&word=%E6%96%8B%E8%97%A4%E9%A3%9E%E9%B8%9F']

    def parse(self, response):
        result = urllib.request.urlopen(self.start_urls[0]).read().decode('utf-8')
        match = re.findall(r'thumbURL(.*?jpg)', result)
        img = BaiduItem()
        for i in match:
        	img['image_url'] = i[3:]
        	img['image_name'] = i.split('/')[-1].split('.')[-2]
        	yield img
