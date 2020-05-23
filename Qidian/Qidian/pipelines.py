# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from openpyxl import Workbook


class QidianPipeline(object):
    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['小说名','小说链接','作者','类型','情况','简介'])
    def process_item(self, item, spider):
        data = [item["novel_name"], item["novel_link"], item["novel_author"], item["novel_type"], item["novel_status"],
                item["novel_intro"]]
        self.ws.append(data)  # 将数据以行的形式添加到工作表中
        self.wb.save('novel.xlsx')  # 保存
        return item
