# -*- coding: utf-8 -*-
"""
项目：爬取CSDN文章内容
作者：cho
时间：2019.9.17
版本：3.0
"""
import scrapy
import requests
import time
from scrapy import Request
import parsel
#import tomd
import json
from CSDN.items import CsdnItem
# import tomd
import json
import time

import parsel
import requests
import scrapy
from scrapy import Request

from CSDN.items import CsdnItem


class CsdnSpider(scrapy.Spider):
    name = 'csdn'
    allowed_domains = ['csdn.net']
    header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    }
    url = 'https://www.csdn.net/api/articles?type=more&category=python&shown_offset=0'

    def start_requests(self):
        url_time = int(time.time() * 1000000)
        urls = self.url + str(url_time)
        yield Request(url=urls, headers=self.header,callback=self.parse)

    def parse(self, response):

        datas = json.loads(response.text)["articles"]

        if datas and len(datas) > 0:
            for article in datas:
                link = str(article['url'])
                read_con = '阅读数' + str(article['views'])
                shown_offset = article['shown_offset']
                item = CsdnItem(read_count=read_con,link=link)
                yield Request(url=link, headers=self.header, callback=self.parse_get_content,meta={'keys':item})  # ,meta={'keys':item}
            time.sleep(0.5)
            next_url = self.url + str(shown_offset)
            if next_url is not None:
                yield Request(url=next_url, headers=self.header, callback=self.parse)

    def parse_get_content(self, response):
        item = response.meta['keys']
        response = requests.get(item['link'])
        sel = parsel.Selector(response.text)
        #print(response.text)
        #c = json.loads(response.text)

        item['title'] = sel.xpath('//div[@class="article-title-box"]/h1/text()').extract_first()
        item['date'] = sel.xpath('//div[@class="article-info-box"]/div/span[@class="time"]/text()').extract_first()
        item['author'] = sel.xpath('//div[@class="article-info-box"]/div/a[@class="follow-nickName"]/text()').extract_first()
        item['column'] = sel.xpath('normalize-space(//div[@class="article-info-box"]/div/div[@class="tags-box space"]/a/text())').extract_first()
        text = sel.css('article').get()
        #content = tomd.Tomd(text).markdown
        #item['content'] = c['data']['markdowncontent']
        item['content'] = text
        yield item









