# -*- coding: utf-8 -*-
"""
项目：爬取起点小说网
作者：cho
时间：2019.9.3-9.4
"""
#from __future__ import absolute_import
import sys
sys.path.append("..")
#sys.path.append(r"D:\HZSR-Work\untitled\Qidian\novel")
#sys.path.append("../")
import scrapy
from Qidian.items import QidianItem

# from ..items import QidianItem
#from Qidian.Qidian.items import Qidian
#sys.path.insert(0, '..')


class QidianSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.qidian.com/all?']
    start_urls = ['https://www.qidian.com/all?orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page=%s' % p for p in range(1,7)]


    def parse(self, response):
        novel_list = response.xpath('//div[@class="book-mid-info"]')
        #next_page = response.xpath('//*[@id="page-container"]/div/ul/li/a//@href').extract_first()

        for i in novel_list:
            item =  QidianItem()

            item['novel_name'] = i.xpath('./h4/a/text()').extract_first()
            item['novel_link'] = "https:" + i.xpath('./h4/a/@href').extract()[0]
            item['novel_author'] = i.xpath('./p[@class="author"]/a[@class="name"]/text()').extract_first()
            item['novel_type'] = i.xpath('./p[@class="author"]/a[@class="go-sub-type"]/text()').extract_first()
            item['novel_status'] = i.xpath('./p[@class="author"]/span/text()').extract_first()
            item['novel_intro'] = i.xpath('./p[@class="intro"]/text()').extract_first()
            #item['novel_word_num'] = i.xpath('./p[@calss="update"]/span/span/text()')[0].strip('万字').extract_first()
            yield item



