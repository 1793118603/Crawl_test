# -*- coding: utf-8 -*-
"""
项目：爬取开源中国开源软件信息
作者：cho
时间：2019.9.23
"""
import parsel
import scrapy

from OSCHINA.items import OschinaItem


class OschinaSpider(scrapy.Spider):
    name = 'oschina'
    allowed_domains = ['oschina.net']


    def start_requests(self):
        for p in range(1,200):
            urls = 'https://www.oschina.net/project/widgets/_project_list?company=0&tag=0&lang=0&os=0&sort=time&recommend=false&cn=false&weekly=false&p={}&type=ajax'.format(p)
            yield scrapy.Request(url=urls,callback=self.parse)

    def parse(self, response):

        lists = response.xpath('//*[@class="item project-item"]')

        for i in lists:
            title = i.xpath('./div/h3/a/@title').extract_first()
            intro = i.xpath('./div/div[1]/p/text()').extract_first()
            collect = i.xpath('./div/div[2]/div/div[1]/text()').extract_first()
            comment = i.xpath('./div/div[2]/div/div[2]/a/text()').extract_first()
            link = i.xpath('./div/h3/a/@href').extract()[0]
            item = OschinaItem(title=title,intro=intro,collect=collect,comment=comment)
            yield scrapy.Request(url=link,callback=self.parse_content,meta={'keys':item})

            #ValueError: Missing scheme in request url: []  TypeError: Request url must be str or unicode, got SelectorList

    def parse_content(self,response):

        item = response.meta['keys']
        sel = parsel.Selector(response.text)

        item['tags'] = sel.xpath('//div[@class="tags"]/a/text()').extract_first()

        info_list = sel.xpath('//div[@class="info-list"]')
        box1 = info_list.xpath('./div[1]/div[@class="info-item"]')
        box2 = info_list.xpath('./div[2]/div[@class="info-item"]')
        if len(box1) == 2:
            license = box1[0].xpath('./span/a/text()')
            item['language'] = '无'
            if len(license):
                item['license'] = box1[0].xpath('./span/a/text()').extract_first()
            else:
                item['license'] = box1[0].xpath('./span/text()').extract_first()

            item['os'] = box1[1].xpath('./span/text()').extract_first()

        elif len(box1) == 3:
            license = box1[0].xpath('./span/a/text()')

            if len(license):
                item['license'] = box1[0].xpath('./span/a/text()').extract_first()
            else:
                item['license'] = box1[0].xpath('./span/text()').extract_first()

            item['language'] = box1[1].xpath('./span/a/text()').extract_first()
            item['os'] = box1[2].xpath('./span/text()').extract_first()

        if len(box2) == 2:
            item['developer'] = '无'
            item['date'] = box2[0].xpath('./span/text()').extract_first()
            item['submitter'] = box2[1].xpath('./span/a/text()').extract_first()

        elif len(box2) == 3:

            item['developer'] = box2[0].xpath('./span/a/text()').extract_first()
            item['date'] = box2[1].xpath('./span/text()').extract_first()
            item['submitter'] = box2[2].xpath('./span/a/text()').extract_first()


        text = sel.css('.project-detail-container').get()
        item['content'] = text
        #item['obj_url'] = sel.xpath('//div[@class="osc_git_title"]/h3/div[2]/a/@href').extract_first()
        yield item



