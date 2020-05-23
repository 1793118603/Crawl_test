# -*- coding: utf-8 -*-
"""
项目：爬取掘金客户信息
作者：cho
时间：2019.9.19
"""
import json

import scrapy
from scrapy import Request

from JUEJIN.items import JuejinItem


class JuejinSpider(scrapy.Spider):
    name = 'juejin'
    allowed_domains = ['juejin.im']
    start_urls = ['https://juejin.im/user/5875dfc7a22b9d0058a96d06']

    def parse(self, response):
        item = JuejinItem()

        info = response.xpath('//div[@class="info-box info-box"]')
        url = response.xpath("//meta[@itemprop='url']/@content").extract()

        uid = url[0].replace('https://juejin.im/user/', '')
        name = info.xpath('./div[1]/h1/text()').extract_first()
        jod = info.xpath('./div[2]/span/span[1]/text()').extract_first()
        intro = info.xpath('./div[3]/span/text()').extract_first()

        follows = response.xpath('//div[@class="follow-block block shadow"]')

        follow = follows.xpath('./a[1]/div[2]/text()').extract_first()
        follows = follows.xpath('./a[2]/div[2]/text()').extract_first()

        item['name'] = name
        item['link'] = url
        item['job'] = jod
        item['intro'] = intro
        item['follow'] = follow
        item['follower'] = follows
        yield item

        #自己关注的用户
        followee_url = 'https://follow-api-ms.juejin.im/v1/getUserFolloweeList?uid='+ uid+'&src=web'
        yield Request(url=followee_url,callback=self.parse_get_url,meta={'uid':uid,'type':'followee'})
        #关注自己的用户
        follower_url = 'https://follow-api-ms.juejin.im/v1/getUserFollowerList?uid=' + uid +'&src=web'
        yield Request(url=follower_url,callback=self.parse_get_url,meta={'uid':uid,'type':'follower'})

    def parse_get_url(self,response):
        obj = json.loads(response.text)
        uid = response.meta['uid']
        type = response.meta['type']
        users = obj.get('d')
        if len(users) > 0:
            for user in users:
                urls = 'https://juejin.im/user/'+ user.get(type).get('objectId')
                yield Request(url=urls,callback=self.parse)
        if len(users) == 20:
            before = users[-1].get('updatedAtString')
            if type =='follower':
                url = 'https://follow-api-ms.juejin.im/v1/getUserFollowerList?uid='+ uid +'&before'+before+'&src=web'
            else:
                url = 'https://follow-api-ms.juejin.im/v1/getUserFolloweeList?uid='+ uid +'&before'+before+'&src=web'
            yield Request(url=url,callback=self.parse_get_url,meta={'uid':uid,'type':type})
#     def insert(self):
#         conn = pymysql.connect(
#             host="sh-cdb-khe0u424.sql.tencentcdb.com",
#             db='srtestdb',
#             user='srtest',
#             password='srtest123',
#             port=62624,
#             charset='utf8'
#         )
#         cursor = conn.cursor()
#         insert = "INSERT INTO JUEJIN VALUES ('%s','%s','%s','%s','%s','%s')" % (
#             item['name'], item['link'], item['job'], item['intro'], item['follow'], item['follower'])
#         cursor.execute(insert)
#         conn.commit()
#         cursor.close()
#         conn.close()
# if __name__ =='__main__':
#     ji = JuejinSpider()
#     ji.parse()
#     ji.parse_get_url()
#     ji.insert()






