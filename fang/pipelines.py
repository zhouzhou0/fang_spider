# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fang import settings
import pymysql
from fang.items import NewhouseItem,EsfhouseItem

MYSQL_HOST=settings.MYSQL_HOST
MYSQL_USER=settings.MYSQL_USER
MYSQL_PASSWORD=settings.MYSQL_PASSWORD
MYSQL_PORT=settings.MYSQL_PORT
MYSQL_DB=settings.MYSQL_DB


class FangPipeline(object):
    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=MYSQL_HOST,  # 数据库地址
            port=MYSQL_PORT,  # 数据库端口
            db=MYSQL_DB,  # 数据库名
            user=MYSQL_USER,  # 数据库用户名
            passwd=MYSQL_PASSWORD,  # 数据库密码
            charset='utf8',  # 编码方式
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()



    def process_item(self, item, spider):
        if isinstance(item, NewhouseItem):
            item=dict(item)
            sql='insert into Newhouse values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,(
               item['province'],
               item['city'],
               item['price'],
               item['state'],
               item['area'],
               item['address'],
               item['rooms'],
               item['cell_name'],
               item['origin_url'],

            ))
            self.connect.commit()
        elif isinstance(item, EsfhouseItem):
            item=dict(item)
            sql='insert into Esfhouse values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,(
               item['province'],
               item['city'],
               item['cell_name'],
               item['address'],
               item['rooms'],
               item['floor'],
               item['toward'],
               item['year'],
               item['area'],
               item['price'],
               item['unit'],
               item['origin_url'],

            ))
            self.connect.commit()

        return item
