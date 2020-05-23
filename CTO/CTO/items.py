# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CtoItem(scrapy.Item):
    #文章标题
    title = scrapy.Field()
    #简介
    info = scrapy.Field()
    #文章链接
    link = scrapy.Field()
    #发布时间
    time = scrapy.Field()
    #阅读数
    count = scrapy.Field()
    #文章内容
    content = scrapy.Field()
    #文章作者
    author = scrapy.Field()