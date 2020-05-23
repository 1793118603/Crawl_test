# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #小说名
    novel_name = scrapy.Field()
    #小说链接
    novel_link = scrapy.Field()
    #作者
    novel_author = scrapy.Field()
    #小说类型
    novel_type = scrapy.Field()
    #小说情况
    novel_status = scrapy.Field()
    #小说简介
    novel_intro = scrapy.Field()
    #小说字数
    #novel_word_num = scrapy.Field()
