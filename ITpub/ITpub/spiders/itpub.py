# -*- coding: utf-8 -*-
"""
项目：爬取ITpub文章信息
作者：cho
时间：2019.9.16
"""
import parsel
import scrapy
from scrapy import Request

from ITpub.items import ItpubItem


class ItpubSpider(scrapy.Spider):
    name = 'Itpub'
    allowed_domains = ['blog.itpub.net']
    #start_urls = ['http://blog.itpub.net/python/']
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }
    # def get_url(self):
    #     for j in range(2, 21):
    #         base_urls = 'http://blog.itpub.net/blog/getmore/70/?page={0}'.format(j)
    #         return base_urls

    def start_requests(self):
        for i in range(1,121):
            url = 'http://blog.itpub.net/python/{}'.format(i)
            yield Request(url=url, headers=self.header, callback=self.parse)


    def parse(self, response):
        list = response.xpath('//li[@class="list-item"]')
        for i in list:
            info = i.xpath('./p/text()').extract_first()
            link = i.xpath('./a/@href').extract_first()
            read_count = i.xpath('./div/span[3]/text()').extract_first()
            type = i.xpath('./div/span[2]/a/text()').extract_first()
            author = i.xpath('./div/span[1]/a/text()').extract_first()
            time = i.xpath('./div/span[4]/text()').extract_first()
            item = ItpubItem(link=link,info=info,read_count=read_count,type=type,author=author,time=time)
            yield Request(url=link,headers=self.header,callback=self.parse_content,meta={'keys':item})


    def parse_content(self,response):

        item = response.meta['keys']
        article_list = response.xpath('//div[@class="preview-header"]')
        sel = parsel.Selector(response.text)
        for i in article_list:
            item['title'] = i.xpath('./h1/text()').extract_first()
            item['content'] = sel.css('body').get()
            yield item
