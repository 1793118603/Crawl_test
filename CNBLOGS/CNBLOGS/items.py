# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #排行
    num = scrapy.Field()
    #作者
    author = scrapy.Field()
    #作者链接
    link = scrapy.Field()
    #发布时间
    #time = scrapy.Field()
    #博客标题
    title = scrapy.Field()
    #博客链接
    url = scrapy.Field()
    #导读
    #info = scrapy.Field()
    #基本信息
    desc = scrapy.Field()
