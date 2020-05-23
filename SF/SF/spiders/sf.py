# -*- coding: utf-8 -*-
"""
项目：爬取思否网站活跃用户信息
作者：cho
时间：2019.9.20
"""
import parsel
import scrapy
from scrapy import Request

from SF.items import SfItem


class SfSpider(scrapy.Spider):
    name = 'sf'
    allowed_domains = ['segmentfault.com']
    start_urls = ['http://segmentfault.com/users']


    def parse(self, response):
        #item = SfItem()
        sel = parsel.Selector(response.text)
        user_list =sel.xpath('//div/ol[@class="widget-top10 col-md-6"]/li')

        for u in user_list:
            img_url = u.xpath('./a/img/@src').extract_first()
            user_url = "https://segmentfault.com"+u.xpath('./a/@href').extract_first()
            name = u.xpath('./a/span/text()').extract_first()
            active = u.xpath('./span/text()').extract_first()
            item = SfItem(img_url=img_url,user_url=user_url,name=name,active=active)
            yield Request(url=str(user_url),callback=self.parse_detail,meta={'keys':item})

    def parse_detail(self,response):
        item = response.meta['keys']
        sel = parsel.Selector(response.text)
        content = sel.xpath('//div[@class="col-md-5 col-sm-9 col-xs-9"]')

        item['profile'] = content.xpath('./div[1]/a/span[1]/text()').extract_first()
        school_con = content.xpath('./div[2]/span[2]/span/text()').extract()
        if len(school_con)>0:
            item['school'] = school_con[0]
            item['major'] = school_con[1]

        company = content.xpath('./div[2]/span[3]/span/text()').extract()
        if len(company)>0:
            item['company'] = company[0]
            item['job'] = company[1]

        item['web_url'] = content.xpath('./div[2]/span[4]/span/a/@href').extract_first()

        item['follow'] = sel.xpath('//div[@class="profile__heading-info row"]/div[1]/a/span[2]/text()').extract_first()
        item['fan'] = sel.xpath('//div[@class="profile__heading-info row"]/div[2]/a/span[2]/text()').extract_first()

        yield item

