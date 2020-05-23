# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsdnItem(scrapy.Item):
    #文章标题
    title = scrapy.Field()
    #发布时间
    date = scrapy.Field()
    #作者
    author = scrapy.Field()
    #阅读数
    read_count = scrapy.Field()
    #文章专栏
    column = scrapy.Field()
    #文章内容
    content = scrapy.Field()
    #文章链接
    link = scrapy.Field()
