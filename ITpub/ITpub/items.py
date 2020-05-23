# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ItpubItem(scrapy.Item):
    #标题
    title = scrapy.Field()
    #简介
    info = scrapy.Field()
    #作者
    author = scrapy.Field()
    #类别
    type = scrapy.Field()
    #发布时间
    time = scrapy.Field()
    #文章链接
    link = scrapy.Field()
    #阅读数
    read_count = scrapy.Field()
    #网页内容
    content = scrapy.Field()

