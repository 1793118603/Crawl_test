"""
项目：国家企业信用公示系统爬取科技有限公司信息(反爬虫)
编程：cho
时间：2019.8.29-9.30
版本：3.0
"""

import requests
import json
import time,re
import execjs
import random
import pymysql
import pandas as pd
from io import BytesIO
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from lxml import etree
import parsel
import urllib
from bs4 import BeautifulSoup
from chaojiying import Chaojiying_Client

BORDER = 6

CHAOJIYING_USERNAME = '账号'
CHAOJIYING_PASSWORD = '密码'
CHAOJIYING_SOFT_ID = '901300'
CHAOJIYING_KIND = '9102'
CHAOJIYING_KIND_FOUR = 9004
CHAOJIYING_KIND_FIVE = 9008  # 5~8 9008

class enterpriseSpider(object):

    def __init__(self):

        chrome_option = webdriver.ChromeOptions()

        self.driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",chrome_options=chrome_option)
        self.driver.set_window_size(1440, 900)
        self.wait = WebDriverWait(self.driver, 10)
        self.cookie_url = 'http://www.gsxt.gov.cn/index.html'
        self.post_url = 'http://www.gsxt.gov.cn/corp-query-search-1.html'
        self.session = requests.Session()
        self.refer_url = 'http://www.gsxt.gov.cn'
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        self.chaojiying = Chaojiying_Client(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
        self.dbconn = pymysql.connect(
            host="sh-cdb-khe0u424.sql.tencentcdb.com",
            db='srtestdb',
            user='srtest',
            password='srtest123',
            port=62624,
            charset='utf8'
        )
        sql = '''select * from HZQY;'''
        a = pd.read_sql(sql, self.dbconn)
        self.keys = a['企业名称']
        self.cursor = self.dbconn.cursor()
        #self.searchword = searchword
        self.detail_list = []
        self.table = '企业信息'

    def get_cookie(self):
        """
        获取 cookies
        :return:
        """
        response = self.session.get(self.cookie_url)
        time.sleep(10)
        js_code1 = response.text
        #print(js_code1)

        js_code1 = js_code1.rstrip('\n')
        js_code1 = js_code1.replace('</script>', '')
        js_code1 = js_code1.replace('<script>', '')
        index = js_code1.rfind('}')
        js_code1 = js_code1[0:index + 1]
        js_code1 = 'function getCookie() {' + js_code1 + '}'
        js_code1 = js_code1.replace('eval', 'return')

        js_code2 = execjs.compile(js_code1)
        code = js_code2.call('getCookie')
        code = 'var a' + code.split('document.cookie')[1].split("Path=/;'")[0] + "Path=/;';return a;"
        code = 'window = {}; \n' + code
        js_final = "function getClearance(){" + code + "};"
        js_final = js_final.replace("return return", "return eval")
        ctx = execjs.compile(js_final)
        jsl_clearance = ctx.call('getClearance')
        jsl_cle = jsl_clearance.split(';')[0].split('=')[1]
        self.session.cookies['__jsl_clearance'] = jsl_cle

    def vist_html(self):

        self.driver.get(self.cookie_url)

        # 查询数据
        self.detail()


    def detail(self):

        for searchword in self.keys:
            # 输入关键字
            time.sleep(3)
            self.driver.find_element_by_id('keyword').send_keys(searchword)
            # 设置延迟
            #selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element
            #运行太快，页面还未完全加载
            # 判断某个元素中是否可见并且是enable的，代表可点击
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.ID, 'btn_query')))
            reg_element = self.driver.find_element_by_id('btn_query')
            reg_element.click()

            # 判断验证码类型
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_commit_tip"]')))
                print('点触验证')
                self.touch()
            except Exception:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="geetest_slider_button"]')))
                print('滑动验证')
                self.analog_drag()

            except Exception:
                print('无验证，直接查询')

            try:

                time.sleep(3)
                now_handle = self.driver.current_window_handle  # 获取当前窗口句柄
                WebDriverWait(self.driver, 10, 0.5).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[@class="search_list_item db"]')))
                self.driver.find_element_by_xpath('//a[@class="search_list_item db"]').click()
                all_windows = self.driver.window_handles
                serach_window = all_windows[-1]  # 切换到最新窗口
                self.driver.switch_to_window(serach_window)
                html = self.driver.page_source
                # print(html)
                # soup = BeautifulSoup(html, 'lxml')
                sel = parsel.Selector(html)  # 解析网页
                content = sel.xpath('//div[@class="overview"]')

                for s in content:
                    #dic = {}

                    name = s.xpath('./dl[2]/dd/text()').extract_first()
                    statu = s.xpath('./dl[11]/dd/text()').extract_first()
                    code = s.xpath('normalize-space(./dl[1]/dd/text())').extract_first()
                    person = s.xpath('./dl[4]/dd/text()').extract_first()
                    capital = s.xpath('normalize-space(./dl[5]/dd/text())').extract_first()
                    office = s.xpath('./dl[9]/dd/text()').extract_first()
                    date = s.xpath('./dl[6]/dd/text()').extract_first()
                    adress = s.xpath('./dl[12]/dd/text()').extract_first()
                    content = sel.css('.page').get()
                    #self.detail_list.append(dic)
                    time.sleep(random.randint(10, 20))
                    self.detail_list = [name,statu,code,person,capital,office,date,adress,content]
                    print(self.detail_list)
                    sql = u"INSERT INTO {table} VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(table=self.table)
                    self.cursor.execute(sql,self.detail_list)
                    self.dbconn.commit()
                    print('成功插入数据！')
                    self.detail_list.clear()
                    self.driver.close()
                self.driver.switch_to_window(now_handle)  # 切换到原来窗口
                time.sleep(0.5)
                WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="menu_item db l tc wh rel"]')))
                reg_element = self.driver.find_element_by_xpath('//a[@class="menu_item db l tc wh rel"]')
                reg_element.click()
                time.sleep(1)
                shouye = self.driver.current_window_handle
                self.driver.switch_to_window(shouye)  #切换回首页
                # selenium.common.exceptions.NoSuchWindowException: Message: no such window: target window already closed
            except:
                print('错误！')
                continue
        self.cursor.close()
        self.dbconn.close()

    def analog_drag(self):
        try:
            button = self.get_geetest_button()
            button.click()
            time.sleep(1)
            # 确认图片加载完成
            self.wait_pic()
            # 获取滑块
            slider = self.get_slider()
            # 获取带缺口验证码图片
            image1 = self.get_geetest_image('captcha1.png')
            # 获取不带缺口的验证码图片
            self.delete_style()
            image2 = self.get_geetest_image('captcha2.png')
            # self.delete_style_test()
            # 获取缺口位置
            gap = self.get_gap(image2, image1)
            print('缺口位置', gap)
            # 减去缺口位移
            gap -= BORDER
            # 获取移动轨迹
            track = self.get_track(gap)
            print('滑动轨迹', track)
            time.sleep(1)
            # 拖动滑块
            self.move_to_gap(slider, track)
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip'), '验证成功')
            )
            print(success)
            time.sleep(1)
        except:
            print('失败，再来一次')
            self.analog_drag()


    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        # 验证按钮
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_refresh_1')))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        print('img')
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + \
                                   size[
                                       'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.driver.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def delete_style(self):
        '''
        执行js脚本，获取无滑块图
        :return None
        '''
        js = 'document.querySelectorAll("canvas")[2].style=""'
        self.driver.execute_script(js)

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 带缺口图片
        :param image2: 不带缺口图片
        :return:
        """
        left = 60
        print(image1.size[0])
        print(image1.size[1])
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0
        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 2
            else:
                # 加速度为负3
                a = -1
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def wait_pic(self):
        '''
        等待验证图片加载完成
        :return None
        '''
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'.geetest_wrap'))
        )


    def get_touclick_element(self):
        """
        获取验证图片对象
        :return: 图片对象，图片链接
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_item_img')))
        url_http = element.get_attribute('src')
        print(url_http)
        return element, url_http

    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            print(location)
            element, url_http = self.get_touclick_element()
            ActionChains(self.driver).move_to_element_with_offset(element, location[0],location[1]).click().perform()
            time.sleep(0.5)

    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_commit_tip')))
        button.click()

    def request_download(self, IMAGE_URL):
        '''
        获取图片链接转换字节流，传入超级鹰
        :return:
        '''
        r = requests.get(IMAGE_URL)
        res = requests.get(IMAGE_URL, stream=True)  # 获取字节流最好加stream这个参数,原因见requests官方文档

        byte_stream = BytesIO(res.content)  # 把请求到的数据转换为Bytes字节流

        roiImg = Image.open(byte_stream)  # Image打开Byte字节流数据
        # roiImg.show()   #  弹出 显示图片
        imgByteArr = BytesIO()  # 创建一个空的Bytes对象

        roiImg.save(imgByteArr, format='PNG')  # PNG就是图片格式，我试过换成JPG/jpg都不行

        imgByteArr = imgByteArr.getvalue()  # 这个就是保存的图片字节流
        with open('img.png', 'wb') as f:
            f.write(r.content)

        return imgByteArr

    # 主函数
    def touch(self):
        try:
            """
            破解入口
            :return: None
            """
            # button = self.get_touclick_button()
            # button.click()
            time.sleep(3)
            # 获取原图地址，保存验证码图片
            element,url_http = self.get_touclick_element()
            img = self.request_download(url_http)
            # 识别验证码
            result = self.chaojiying.PostPic(img, CHAOJIYING_KIND_FIVE)
            print(result)
            # if 'NO' in result['err_str']:
            #     print('题分已经不足请充值')
            #     raise ValueError
            locations = self.get_points(result)
            self.touch_click_words(locations)
            self.touch_click_verify()
            # 判定是否成功
            success = self.wait.until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, 'ads-sci-title'), '信息分类'))
            print(success)
            time.sleep(1)
            print('验证成功')

        except Exception as e:
            print(e)
            pic_id = result.get('pic_id')
            self.chaojiying.ReportError(pic_id)
            print('失败，再次测试')
            self.touch()

    def insert_data(self):
        table = '企业信息'
        for data in self.detail_list:
            keys = ','.join(data.keys())
            values = ','.join(['%s']*len(data))  #TypeError: 'builtin_function_or_method' object is not subscriptable
            sql = 'insert into {table}({keys}) VALUES ({values})'.format(table=table,keys=keys,values=values)
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
        self.get_cookie()
        self.vist_html()
        #self.insert_data()

if __name__ == "__main__":

    spider = enterpriseSpider()
    spider.run()