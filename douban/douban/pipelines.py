# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import pymysql

class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlPipeline(object):
    def insert_information(self, sql):
        connection = pymysql.connect(host='localhost', user='root', password='jn123528', charset='utf8')
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.commit()
        connection.close()

    def process_item(self, item, spider):
        name = item['music_name']
        name = name.replace('"', '')
        info = item['music_info']
        info = info.replace('"', '')
        try:
            descri = item['music_describe']
            descri = descri.replace('"', '')
        except:
            descri = item['music_describe']
        star = item['music_star']
        image_url = item['music_image_url']
        sql = 'insert into music.music(name, info ,descri, star, image_url) values("{}", "{}", "{}", "{}", "{}");'.format(name, info, descri, star, image_url)
        try:
            self.insert_information(sql)
        except:
            print(sql)
            exit(0)