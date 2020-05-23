# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SfItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #图片链接
    img_url = scrapy.Field()
    #主页链接
    user_url = scrapy.Field()
    #用户名
    name = scrapy.Field()
    #活跃值
    active = scrapy.Field()
    #声望
    profile = scrapy.Field()
    #学校
    school = scrapy.Field()
    #专业
    major = scrapy.Field()
    #单位
    company = scrapy.Field()
    #职业
    job = scrapy.Field()
    #个人链接
    web_url = scrapy.Field()
    #关注数
    follow = scrapy.Field()
    #粉丝数
    fan = scrapy.Field()
    #文章发布时间
    date = scrapy.Field()
    #摘要
    excerpt = scrapy.Field()
    #用户ID
    id = scrapy.Field()
    #文章标题
    title = scrapy.Field()
    #文章链接
    a_url = scrapy.Field()
    #点赞数
    votes = scrapy.Field()
    #阅读数
    views = scrapy.Field()
    #专栏名称
    blog_name = scrapy.Field()
    #专栏链接
    blog_url = scrapy.Field()
    #文章内容
    content = scrapy.Field()