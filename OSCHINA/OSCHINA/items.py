# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OschinaItem(scrapy.Item):
    #标题
    title = scrapy.Field()
    #简介
    intro = scrapy.Field()
    #收藏数
    collect = scrapy.Field()
    #评论数
    comment = scrapy.Field()
    #标签
    tags = scrapy.Field()
    #授权协议
    license = scrapy.Field()
    #开发语言
    language = scrapy.Field()
    #开发商
    developer = scrapy.Field()
    #收录时间
    date = scrapy.Field()
    #操作系统
    os = scrapy.Field()
    #提交者
    submitter = scrapy.Field()
    #具体内容
    content = scrapy.Field()
    #项目链接
    #obj_url = scrapy.Field()
