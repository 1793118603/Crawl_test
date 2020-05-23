# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CrawlproPipeline(object):
    def process_item(self, item, spider):
        novel = '{}.txt'.format(item['novel_name'])
        # 动态创建小说的文件
        self.file = open(novel, 'a')
        self.file.write(str(item['chapter_title']) + '\n' + item['content'])
        self.file.close()
