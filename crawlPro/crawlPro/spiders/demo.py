# -*- coding: utf-8 -*-
"""
项目：爬取笔趣阁首页小说内容
作者：cho
时间：2019.9.10
版本：3.0
"""
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from crawlPro.items import CrawlproItem


class DemoSpider(CrawlSpider):
    name = 'demo'
    allowed_domains = ['sbiquge.com']
    start_urls = ['http://sbiquge.com/']

    rules = (
        Rule(LinkExtractor(allow="/\d+?_\d+?/", unique=True), callback='parse_item', follow=False),
    )

    def parse_item(self, response):

        novel_name = response.xpath('//*[@id="book"]/div[1]/div/a[2]/text()').extract_first()
        item = CrawlproItem(novel_name=novel_name)
        link = 'http://sbiquge.com/' + response.xpath('.//*[@class="listmain"]/dl/dd[7]/a/@href').extract_first()
        url = scrapy.Request(url=link,callback=self.parse_body,meta={'key': item})
        yield url



    def parse_body(self,response):
        item = response.meta['key']

        item['chapter_title'] = response.xpath('//*[@class="content"]/h1/text()').extract_first()

        content_list = response.xpath('.//*[@id="content"]').re('([\u4e00-\u9fa5]|<br>)+?')
        content_str = ''.join(content_list)
        content = re.sub('<br><br>', '\n', content_str)
        item['content'] = content
        link = 'http://sbiquge.com/' + response.xpath('//div[@class="page_chapter"]/ul/li[3]/a/@href').extract_first()
        res = scrapy.Request(url=link,callback=self.parse_body,meta={'key':item})
        yield item
        yield res


