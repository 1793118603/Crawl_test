# -*- coding: utf-8 -*-
"""
项目：爬取思否网站首页推荐文章
作者：cho
时间：2019.9.23
"""
import json

import parsel
import scrapy
from scrapy import Request

from SF.items import SfItem


class SfCrawlSpider(scrapy.Spider):
    name = 'sf_crawl'
    allowed_domains = ['segmentfault.com']
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'referer': 'https://segmentfault.com/',
        'content-type': 'application/json; charset=UTF-8',
    }

    def start_requests(self):
        for page in range(1,100):
            urls = 'https://segmentfault.com/api/timelines/recommend?page={}&_=4f2739f6f7dc1221704e01a1dfb7b8c7'.format(page)
            yield Request(url=urls,headers=self.header,callback=self.parse)

    def parse(self, response):

        datas = json.loads(response.text)["data"]

        if datas and len(datas)>0:
            for data in datas:
                name = data['user'][2]
                user_url = 'https://segmentfault.com'+ data['user'][3]
                id = data['user_id']
                title = data['title']
                excerpt = data['excerpt']
                date = data['createdDate']
                views = data['viewsWord']
                votes = data['votes']
                a_url = str('https://segmentfault.com'+ data['url'])
                item = SfItem(name=name,user_url=user_url,id=id,title=title,excerpt=excerpt,date=date,views=views,votes=votes)
                yield Request(url=a_url,headers=self.header,callback=self.parse_content,meta={'keys':item})

    def parse_content(self,response):
        item = response.meta['keys']
        sel = parsel.Selector(response.text)
        item['blog_name'] = sel.xpath('//div[@class="article__authormeta"]/a[2]/text()').extract_first()
        item['blog_url'] = sel.xpath('//div[@class="article__authormeta"]/a[2]/@href').extract_first()
        item['content'] = sel.xpath('div[@class="row"]/text()').extract_first()
        yield item

