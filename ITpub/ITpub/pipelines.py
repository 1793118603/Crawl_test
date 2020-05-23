# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class ItpubPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host="sh-cdb-khe0u424.sql.tencentcdb.com",
            db='srtestdb',
            user='srtest',
            password='srtest123',
            port=62624,
            charset='utf8'
        )
        self.cursor = self.connect.cursor()
    def process_item(self, item, spider):
        insql = "INSERT INTO ITPUB VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')"%(item['title'],item['info'],item['author'],item['type'],item['read_count'],item['time'],item['link'],pymysql.escape_string(item['content']))
        self.cursor.execute(insql)
        self.connect.commit()

    def close_spider(self):
        self.cursor.close()
        self.connect.close()
