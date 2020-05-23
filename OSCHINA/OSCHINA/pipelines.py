# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class OschinaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(
            host="sh-cdb-khe0u424.sql.tencentcdb.com",
            db='srtestdb',
            user='srtest',
            password='srtest123',
            port=62624,
            charset='utf8'
        )
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql = "INSERT INTO OSCHINA VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s);"
        list =[item['title'],item['submitter'],item['date'], item['intro'], item['tags'], item['license'],item['language'],item['os'],item['developer'],pymysql.escape_string(item['content']),item['collect'],item['comment']]
        self.cursor.execute(insert_sql,list)

        # 4. 提交操作
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
