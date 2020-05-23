# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JuejinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #用户名
    name = scrapy.Field()
    #用户链接
    link = scrapy.Field()
    #职业
    job = scrapy.Field()
    #介绍
    intro = scrapy.Field()
    #关注
    follow = scrapy.Field()
    #被关注
    follower = scrapy.Field()


