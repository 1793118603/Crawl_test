# -*- coding: utf- scrapy

"""
项目：爬取链家网(杭州所有二手房成交信息)
作者：cho
时间：2019.9.5
"""
import sys
sys.path.append("..")
from scrapy import Spider,Request
from lxml import etree
import json
from urllib.parse import quote
from Lianjia.items import LianjiaItem


class LianjiaSpider(Spider):
    name = 'lianjia'
    allowed_domains = ['hz.lianjia.com']
    regions = {
        'xihu':'西湖',
        'dajiangdong1':'大江东',
        'qiantangxinqu':'钱塘新区',
        'xiaxheng':'下城',
        'jianggan':'江干',
        'gongshu':'拱墅',
        'shangcheng':'上城',
        'binjiang':'滨江',
        'yuhang':'余杭',
        'xiaoshan':'萧山',
        'tonglu1':'桐庐',
        'chunan1':'淳安',
        'jiande':'建德',
        'fuyang':'富阳',
        'linan':'临安'
    }
    headers = {
        'User - Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 76.0.3809.132Safari / 537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept - Language': 'zh - CN, zh;q = 0.9',
        'Connection': 'keep - alive'
    }

    def start_requests(self):
        for region in list(self.regions.keys()):
            url = "https://hz.lianjia.com/xiaoqu/"+ region+"/"
            yield Request(url=url,headers=self.headers,callback=self.parse,meta={'region':region})

    def parse(self, response):
        region = response.meta['region']
        selector = etree.HTML(response.text)
        sel = selector.xpath('//div[@class="page-box house-lst-page-box"]/@page-data')[0] #返回为字符串
        #转化为字典
        sel = json.loads(sel)
        total_pages = sel.get("totalPage")

        for i in range(int(total_pages)):
            url_page = "https://hz.lianjia.com/xiaoqu/{}/pg{}/".format(region, str(i + 1))
            yield Request(url = url_page,callback=self.parse_xiaoqu,meta = {'region':region})


    def parse_xiaoqu(self,response):
        selector = etree.HTML(response.text)
        xiaoqu_list = selector.xpath('//ul[@class="listContent"]//li//div[@class="title"]/a/text()')
        for xq_name in xiaoqu_list:
            url = "https://hz.lianjia.com/chengjiao/rs"+ quote(xq_name) + "/"
            yield Request(url =url,headers = self.headers,callback=self.parse_chengjiao,meta={'xq_name':xq_name,
                                                                       'region':response.meta['region']})
    def parse_chengjiao(self,response):
        xq_name = response.meta['xq_name']
        selector = etree.HTML(response.text)
        content = selector.xpath("//div[@class='page-box house-lst-page-box']")
        total_pages = 0
        if(len(content)):
            page_data = json.loads(content[0].xpath('./@page-data')[0])
            total_pages = page_data.get("totalPage")
        for i in range(int(total_pages)):
            url_page = "https://hz.lianjia.com/chengjiao/pg{}rs{}/".format(str(i + 1), quote(xq_name))
            yield Request(url=url_page,headers = self.headers, callback=self.parse_content, meta={'region': response.meta['region']})

    def parse_content(self,response):
        selector = etree.HTML(response.text)
        cj_list = selector.xpath("//ul[@class='listContent']/li")

        for cj in cj_list:
            item = LianjiaItem()
            item['region'] = self.regions.get(response.meta['region'])
            href = cj.xpath('./a/@href')
            if not len(href):
                continue
            item['href'] = href[0]

            content = cj.xpath('.//div[@class="title"]/a/text()')
            if len(content):
                content = content[0].split()  # 按照空格分割成一个列表
                item['name'] = content[0]
                item['style'] = content[1]
                item['area'] = content[2]

            content = cj.xpath('.//div[@class="houseInfo"]/text()')
            if len(content):
                content = content[0].split('|')
                item['orientation'] = content[0]
                item['decoration'] = content[1]
                if len(content) == 3:
                    item['elevator'] = content[2]
                else:
                    item['elevator'] = '无'

            content = cj.xpath('.//div[@class="positionInfo"]/text()')
            if len(content):
                content = content[0].split()
                item['floor'] = content[0]
                if len(content) == 2:
                    item['build_year'] = content[1]
                else:
                    item['build_yaer'] = '无'

            content = cj.xpath('.//div[@class="dealDate"]/text()')
            if len(content):
                item['sign_time'] = content[0]

            content = cj.xpath('.//div[@class="totalPrice"]/span/text()')
            if len(content):
                item['total_price'] = content[0] + '万'

            content = cj.xpath('.//div[@class="unitPrice"]/span/text()')
            if len(content):
                item['unit_price'] = content[0] + '元/平'

            content = cj.xpath('.//div[@class="dealHouseTxt"]/span/text()')
            if len(content):
                for i in content:
                    if i.find("房屋满") != -1:  # 找到了返回的是非-1得数，找不到的返回的是-1
                        item['fangchan_class'] = i
                    elif i.find("近地铁") != -1:
                        item['subway'] = i
                    elif i.find("学") != -1:
                        item['school'] = i
            yield item



