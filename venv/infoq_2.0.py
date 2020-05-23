"""
项目：infoq热点文章爬取
作者：cho
时间：2019.10.8
版本：2.0
"""

from selenium import webdriver
import requests
import parsel
import time
import pymysql
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class infoqSpider(object):

    def __init__(self):
        chrome_option = webdriver.ChromeOptions()
        #chrome_option.add_argument('--headless')  # 设置成无头浏览器
        self.driver = webdriver.Chrome(
            executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
            chrome_options=chrome_option)
        self.driver.set_window_size(1440, 900)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = 'https://www.infoq.cn/hotlist?tag=day'
        self.session = requests.Session()
        # self.dbconn = pymysql.connect(
        #     host="sh-cdb-khe0u424.sql.tencentcdb.com",
        #     db='srtestdb',
        #     user='srtest',
        #     password='srtest123',
        #     port=62624,
        #     charset='utf8'
        # )
        # self.cursor = self.dbconn.cursor()
        self.table = 'INFOQ'

    def visthtml(self):
        self.driver.get(self.url)
        for i in range(0, 11):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            try:
                self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="more-button _3onsJjulw_ZjgvJO5gfULb_0"]')))
                self.driver.find_element_by_xpath('//div[@class="more-button _3onsJjulw_ZjgvJO5gfULb_0"]').click()
                print('点击加载')
                i += 1
                time.sleep(4)
                self.detail()
            except:
                i += 1
                time.sleep(4)
                self.detail()

    def detail(self):

        html = self.driver.page_source
        sel = parsel.Selector(html)
        articles = sel.xpath('//div[@class="list-item image-position-right"]')
        takes = []
        for a in articles:
            dic = {}
            dic['图片链接'] = a.xpath('./div[1]/img/@src').extract_first()
            dic['文章标题'] = a.xpath('normalize-space(./div[2]/h6/a/text())').extract_first()
            dic['文章链接'] = 'https://www.infoq.cn/'+ a.xpath('./div[2]/h6/a/@href').extract_first()
            dic['摘要'] = a.xpath('./div[2]/p[1]/text()').extract_first()
            author = a.xpath('./div[2]/p[2]/a/text()')
            if author:
                dic['作者'] = author.extract_first()
            else:
                dic['作者'] = a.xpath('./div[2]/p[2]/text()').extract_first()

            dic['时间'] = a.xpath('normalize-space(./div[2]/div[2]/div[2]/text())').extract_first()
            takes.append(dic)
        print(takes)
        return takes

    def insert_data(self):
        detail_list = self.detail()
        for data in detail_list:
            keys = ','.join(data.keys())
            values = ','.join(['%s']*len(data))  #TypeError: 'builtin_function_or_method' object is not subscriptable
            sql = 'insert into {table}({keys}) VALUES ({values})'.format(table=self.table,keys=keys,values=values)
            # update = ','.join(['{key}=%s'.format(key=key) for key in data])
            # sql += update
            try:
                if self.cursor.execute(sql,tuple(data.values())):
                    print('insert successful')
                self.dbconn.commit()
            except Exception as e:
                print("insert failed!", e)
                self.dbconn.rollback()
        self.dbconn.close()

    # 程序完成，自动结束程序
    def __del__(self):
        self.driver.close()

    def run(self):
        self.visthtml()
        #self.insert_data()

if __name__ == "__main__":

    spider = infoqSpider()
    spider.run()