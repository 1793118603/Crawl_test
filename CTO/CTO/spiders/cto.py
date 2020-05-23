# -*- coding: utf-8 -*-
"""
项目：爬取51CTO网站博客信息
作者：cho
时间：2019.9.17
"""
import parsel
import re
import scrapy
from scrapy import Request

from CTO.items import CtoItem


class CtoSpider(scrapy.Spider):
    name = 'cto'
    allowed_domains = ['blog.51cto.com']
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }

    def start_requests(self):
        for i in range(1,32):
            urls = 'https://blog.51cto.com/artcommend/66/p{}'.format(i)
            yield Request(url=urls,headers=self.header,callback=self.parse,)

    def parse(self, response):
        article_list = response.xpath('//ul[@class="artical-list"]/li')
        for a in article_list:
            title = a.xpath('./a/text()').extract_first()
            info = a.xpath('./div[2]/text()').extract_first()
            count = a.xpath('./div[3]/span[1]/text()').extract_first()
            counts = re.sub("\D","",count)
            link = a.xpath('./a/@href').extract_first()
            item = CtoItem(title=title,info=info,count=counts,link=str(link))
            yield Request(url=link,headers=self.header,callback=self.parse_body,meta={'keys':item})

    def parse_body(self,response):
        item = response.meta['keys']
        sel = parsel.Selector(response.text)
        content_con = sel.xpath('//div[@class="artical-Left-blog"]')
        for i in content_con:
            item['author'] = i.xpath('./div[2]/a[1]/text()').extract_first()
            item['time'] = i.xpath('./div[2]/a[@class="time fr"]/text()').extract_first()
            item['content'] = i.xpath('./div[3]/div').extract_first()
            yield item

