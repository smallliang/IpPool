# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import pymysql
from pymysql.cursors import DictCursor
import copy
from scrapy.crawler import Settings as settings

class CollectipsPipeline(object):
    def __init__(self):
        db_params = dict(
            host = "localhost",
            db = "crawed",
            user = "root",
            passwd = "123456",
            charset = "utf8",
            cursorclass = DictCursor,
            use_unicode = True
        )
        # 生成连接池
        self.dbpool = adbapi.ConnectionPool('pymysql', **db_params)
        # self.connect = pymysql.connect(**db_params)
        # self.cursor = self.connect.cursor()

    def insert_into_table(self, conn, item):
        sql = "insert into ippools(ip, port, position, type, speed, last_check_time) values (%s, %s, %s, %s, %s, %s)"
        params = (item['IP'], item['PORT'], item['POSITION'], item['TYPE'], item['SPEED'], item['LAST_CHECK_TIME'])
        conn.execute(sql, params)
        print("存入成功！")

    # 错误处理方法
    def handle_error(self, failure, item, spider):
        print("存入出错")


    def process_item(self, item, spider):
        # sql = "insert into zreading(title, author, pub_date, types, tags, view_counts, content) values (%s, %s, %s, %s, %s, %s, %s)"
        # params = (item['title'], item['author'], item['pub_date'], item['types'], item['tags'], item['view_counts'],
        #           item['content'])
        # self.cursor.execute(sql, params)
        # self.connect.commit()
        asyn_item = copy.deepcopy(item)
        res = self.dbpool.runInteraction(self.insert_into_table, asyn_item)#调用函数插入数据到sql
        res.addErrback(self.handle_error, item, spider) #调用异常处理方法
        return item
