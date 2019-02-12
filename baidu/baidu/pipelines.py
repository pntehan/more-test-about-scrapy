# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
import os
import shutil

class BaiduPipeline(object):
    def process_item(self, item, spider):
        return item

class my_ImagePipeline(ImagesPipeline):
	"""docstring for my_ImagePipeline"""
	img_store = get_project_settings().get('IMAGES_STPORE')

	def get_media_requests(self, item, info):
		yield scrapy.Request(item['image_url'])

	def item_completed(self, results, item, info):
		image_path = [x['path'] for ok, x in results if ok]
		if not image_path:
			raise DropItem('图片地址失效!')
		img_path = self.img_store+'/斋藤飞鸟/'
		if not os.path.exists(img_path):
			os.makedirs(img_path)
		try:
			shutil.move(self.img_store+'/'+image_path[0], img_path+item['image_name']+'.jpg')
		except:
			pass
		item['image_path'] = img_path+item['image_name']+'.jpg'
		return item

	
