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
        name = item['book_name']
        info = item['book_info']
        try:
            descri = item['book_describe']
        except:
            descri = '暂无内容简介...'
        star = item['book_star']
        image_url = item['book_image_url']
        sql = 'insert into book.book(name, info ,descri, star, image_url) values("{}", "{}", "{}", "{}", "{}");'.format(name, info, descri, star, image_url)
        try:
            self.insert_information(sql)
        except:
            print(sql)
            exit(0)