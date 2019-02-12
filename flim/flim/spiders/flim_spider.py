# -*- coding: utf-8 -*-
import scrapy
from flim.items import FlimItem

class FlimSpiderSpider(scrapy.Spider):
    name = 'flim_spider'
    allowed_domains = ['www.80s.tw']
    start_urls = ['https://www.80s.tw/movie/list/---3--p/']

    def parse(self, response):
        content = response.xpath("//*[@id='block3']/div[3]/ul[2]/li/h3/a")
        print('-----------------------------------')
        print(response.request.headers)
        print('-----------------------------------')
        print(response.request.meta)
        print('-----------------------------------')
        if content:
        	for i in content.xpath(".//@href").extract():
        		link = 'https://www.80s.tw'+i
        		yield scrapy.Request(link, callback=self.get_information)
        pages = response.xpath("//*[@id='block3']/div[3]/div/a")
        for i in pages:
        	if i.xpath(".//text()").extract_first() == '下一页':
        		next_page = 'https://www.80s.tw'+i.xpath(".//@href").extract_first()
        		yield scrapy.Request(next_page, callback=self.parse)

    def get_information(self, response):
    	flim = FlimItem()
    	content = response.xpath("//*[@id='block3']/div[2]")
    	if content:
    		info = content.xpath(".//*[@id='minfo']")
    		if info:
    			flim['flim_name'] = info.xpath(".//div[@class='img']/img/@title").extract_first()
    			flim['flim_image_url'] = 'http:'+info.xpath(".//div[@class='img']/img/@src").extract_first()
    			flim['flim_image_name'] = info.xpath(".//div[@class='img']/img/@title").extract_first()
    			flim['flim_info'] = ''
    			flim['flim_describe'] = ''
    			text = info.xpath(".//div[@class='info']/child::*")
    			for i in text[:-2]:
    				for one in i.xpath(".//text()").extract():
    					if not one.split() == []:
    						flim['flim_info'] += "".join(one.split())
    			for i in text[-2:-1]:
    				for one in i.xpath(".//text()").extract():
    					if not one.split() == []:
    						flim['flim_describe'] += "".join(one.split())
    	link = response.xpath("//*[@id='myform']/ul/li[2]/span[1]/span/a/@href").extract_first()
    	if link:
    		flim['flim_url'] = link
    	yield flim
    	

