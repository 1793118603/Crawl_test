# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#import codecs
import pymysql


class CsdnPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
        host="localhost",
        db='mydb',
        user='root',
        password='zqh454596',
        port=3306,
        charset='utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        #article = '{}.md'.format(item['title'])
        # 动态创建文件
        # self.file = codecs.open(article, 'w',encoding='utf-8')
        # self.file.write(str(item['title']) + '\n' + str(item['date']) + '\t' + str(item['author']) + '\n' + str(item['read_count']) + '\n')
        # self.file.write(item['content'])
        # self.file.close()
        insert_sql = "INSERT INTO CSDN VALUES ('%s', '%s', '%s', '%s','%s','%s','%s')" %(item['title'],item['date'],item['author'],item['read_count'],item['column'],item['link'],pymysql.escape_string(item['content']))
        self.cursor.execute(insert_sql)

        # 4. 提交操作
        self.connect.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

