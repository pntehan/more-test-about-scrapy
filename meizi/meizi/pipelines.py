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
import pymysql

class MeiziPipeline(object):
	def process_item(self, item, spider):
		return item

class my_ImagePipeline(ImagesPipeline):
	"""docstring for my_ImagePipeline"""
	img_store = get_project_settings().get('IMAGES_STORE')

	def get_media_requests(self, item, info):
		yield scrapy.Request(item['image_url'])

	def item_completed(self, results, item, info):
		image_path = [x['path'] for ok, x in results if ok]
		if not image_path:
			raise DropItem('图片地址失效!')
		name = item['image_name'].split('第')[0]
		img_path = self.img_store+'/'+name+'/'
		if not os.path.exists(img_path):
			os.makedirs(img_path)
		try:
			shutil.move(self.img_store+'/'+image_path[0], img_path+item['image_name']+'.jpg')
		except:
			pass
		item['image_path'] = img_path+item['image_name']+'.jpg'
		return item

def dbHandle():
	conn = pymysql.connect(
		host = 'localhost',
		user = 'root',
		password = 'jn123528',
		charset = 'utf8',
		use_unicode = False
	)
	return conn

class Mysql_Pipeline(object):
	def process_item(self, item, spider):
		dbObject = dbHandle()
		cursor = dbObject.cursor()
		sql = 'insert into meizi_img.image(image_url, image_name, image_path) values (%s, %s, %s)'
		try:
			cursor.execute(sql, (item['image_url'], item['image_name'], item['image_path']))
			dbObject.commit()
		except Exception as e:
			print(e)
			dbObject.rollback()
