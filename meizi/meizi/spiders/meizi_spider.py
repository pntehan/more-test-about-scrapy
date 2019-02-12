# -*- coding: utf-8 -*-
import scrapy
from meizi.items import MeiziItem

class MeiziSpiderSpider(scrapy.Spider):
	name = 'meizi_spider'
	allowed_domains = ['www.msgao.com']
	start_urls = ['http://www.msgao.com/tag/danai/']

	def parse(self, response):
		content = response.xpath("//html/body/div[5]/div[3]/ul/li/a[1]")
		if content:
			for i in content.xpath(".//@href").extract():
				link = 'http://www.msgao.com' + i
				yield scrapy.Request(link, callback=self.get_information)
		pages = response.xpath("/html/body/div[5]/div[4]/ul/a")
		'''
        for page in pages:
        	if page.xpath(".//text()").extract_first() == '下一页':
        		next_page = 'http://www.msgao.com'+page.xpath(".//@href").extract_first()
        		yield scrapy.Request(next_page, callback=self.parse)
		'''

	def get_information(self, response):
		img = MeiziItem()
		content = response.xpath("//*[@id='contbody']/div[5]/div")
		if content:
			img['image_url'] = content.xpath(".//a[1]/img/@src").extract_first()
			img['image_name'] = content.xpath(".//a[1]/img/@alt").extract_first()
			yield img
			pages = content.xpath(".//div[2]/a")
			for page in pages:
				if page.xpath(".//text()").extract_first() == '下一页':
					next_page = 'http://www.msgao.com'+page.xpath(".//@href").extract_first()
					yield scrapy.Request(next_page, callback=self.get_information)
