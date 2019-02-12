# -*- coding: utf-8 -*-
import scrapy
from movie.items import MovieItem

class MovieSpiderSpider(scrapy.Spider):
    name = 'movie_spider'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['https://www.dytt8.net/html/gndy/china/index.html']

    def parse(self, response):
        content = response.xpath("//*[@id='header']/div/div[3]/div[3]/div[2]/div[2]")
        if content:
        	links = content.xpath(".//div[2]/ul/td/table/tr[2]/td[2]/b/a[2]/@href").extract()
        	for i in links:
        		url = 'https://www.dytt8.net' + i
        		yield scrapy.Request(url, callback=self.get_infomation)
        pages = content.xpath(".//div[2]/div[@class='x']/td/a")
        for page in pages:
        	if page.xpath(".//text()").extract_first() == '下一页':
        		next_page = 'https://www.dytt8.net/html/gndy/china/'+page.xpath(".//@href").extract_first()
        		yield scrapy.Request(next_page, callback=self.parse)
        #yield scrapy.Request('https://www.dytt8.net/html/gndy/dyzz/20180106/55998.html', callback=self.get_infomation)

    def get_infomation(self, response):
    	movie = MovieItem()
    	content = response.xpath("//*[@id='Zoom']/td/p[1]")
    	if content.xpath(".//text()").extract_first() == '\xa0':
    		content = response.xpath("//*[@id='Zoom']/td")
    		text = content.xpath(".//text()").extract()
    		name = "".join(text[3].split())[3:]
    		if '/' in name:
    			movie['movie_name'] = name.split('/')[0]
    		else:
    			movie['movie_name'] = name
    		movie['movie_image'] = content.xpath(".//img/@src").extract_first()
    		describe = ""
    		for i in text[:-24]:
    			describe += "".join(i.split()) + '\n'
    		movie['movie_describe'] = describe
    		movie['movie_url'] = content.xpath(".//table[2]/tbody/tr/td/a/@href").extract_first()
    		yield movie
    	elif content.extract_first() == None:
    		content = response.xpath("//*[@id='Zoom']/td")
    		text = content.xpath(".//text()").extract()
    		name = "".join(text[3].split())[3:]
    		if '/' in name:
    			movie['movie_name'] = name.split('/')[0]
    		else:
    			movie['movie_name'] = name
    		movie['movie_image'] = content.xpath(".//img/@src").extract_first()
    		describe = ""
    		for i in text[:-24]:
    			describe += "".join(i.split()) + '\n'
    		movie['movie_describe'] = describe
    		movie['movie_url'] = content.xpath(".//table/tbody/tr/td/a/@href").extract_first()
    		yield movie
    	else:
    		text = content.xpath(".//text()").extract()
    		name = "".join(text[3].split())[3:]
    		if '/' in name:
    			movie['movie_name'] = name.split('/')[0]
    		else:
    			movie['movie_name'] = name
    		movie['movie_image'] = content.xpath(".//img/@src").extract_first()
    		describe = ""
    		for i in text[:-3]:
    			describe += "".join(i.split()) + '\n'
    		movie['movie_describe'] = describe
    		movie['movie_url'] = content.xpath(".//a/@href").extract_first()
    		yield movie




