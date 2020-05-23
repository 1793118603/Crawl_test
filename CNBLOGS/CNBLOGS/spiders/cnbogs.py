# -*- coding: utf-8 -*-
"""
项目：爬取博客园
作者：cho
时间：2019.9.18
"""
import parsel
import scrapy
from scrapy import Request

from CNBLOGS.items import CnblogsItem


class CnbogsSpider(scrapy.Spider):
    timeout = 10
    name = 'cnbogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/aggsite/UserStats',]

    # custom_settings = {
    #     'LOG_LEVEL': 'DEBUG',
    #     'LOG_FILE': 'CNBLOGS_log_%s.txt' % time.time(),  #配置的日志
    #     "DEFAULT_REQUEST_HEADERS": {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    # }
    # }   #添加的请求头

    def parse(self, response):

        sel = parsel.Selector(response.text)
        blogs_list = sel.xpath('//*[@id="blogger_list"]/ul/li')
        for i in blogs_list:
            num = i.xpath('./text()').extract_first()
            author = i.xpath('./a/text()').extract_first()
            link = i.xpath('./a/@href').extract_first()
            item = CnblogsItem(author=author,link=link,num=num)
            yield Request(url=response.urljoin(link),callback=self.parse_get_body,meta={'keys':item})

    def parse_get_body(self,response):
        item = response.meta['keys']

        article_list = response.xpath('//*[@class="day"]')
        for a in article_list:

            item['title'] = a.xpath('normalize-space(./div[2]/a/text())').extract_first()
            item['url'] = a.xpath('./div[2]/a/@href').extract_first()
            item['desc'] = a.xpath('normalize-space(//div[@class="postDesc"]/text())').extract_first()
            yield item
        for p in range(1, 50):
            next_page = item['link'] + 'default.html?page={}'.format(p)
            yield Request(url=response.urljoin(next_page), callback=self.parse_get_body,meta={'keys':item})

