# -*- coding: utf-8 -*-
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import urllib3
urllib3.disable_warnings()
# from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import cx_Oracle
import string
import zipfile
import re


class MagiSpider(object):

    def __init__(self):

        # 添加ip 代理
        self.proxyHost = " "
        self.proxyPort = " "
        self.proxyUser = " "
        self.proxyPass = " "
        proxy_auth_plugin_path = (self.proxyHost,self.proxyPort,self.proxyUser,self.proxyPass)
        options = Options()
        # options.add_argument('--headless')
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_extension(proxy_auth_plugin_path)

        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                }
        }
        # 添加阻止弹窗
        options.add_experimental_option('prefs', prefs)
        # 添加请求头
        # options.add_argument('uesr-agent="{}"'.format(UserAgent().chrome))
        # options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        # self.baidu_item = baidu_item
        self.waiter = WebDriverWait(self.browser, 20, 0.1)



    def search_keyword(self,item):
        self.browser.get('https://magi.com/')
        # time.sleep(3)

        # 创建等待事件 search-input
        # 创建等待事件
        # 等待登录页登录框被刷新的时间
        event = (By.ID, 'search-input')
        self.waiter.until(EC.presence_of_element_located(event))

        # 获取登陆用户名
        elem = self.browser.find_element_by_id('search-input')
        elem.clear()  # 清空
        elem.send_keys(item['KEYWORD'])  # 自动填充
        elem.send_keys(Keys.RETURN)  # 回车


        # //*[@id="footer"]

        # 获取登陆用户名
        event = (By.ID, 'footer')
        self.waiter.until(EC.presence_of_element_located(event))

    # def keyword(self):

        html = self.browser.page_source

        return html


    def parse_data(self,html):
        items = {}
        # print('1111111111')
        # print(html)
        # print('22222222222')
        # describe
        describe = re.findall(r'<dd data-field="predicate">描述</dd>.*?<dd data-field="object">(.*?)</dd>',html,re.S | re.M)
        # print(describe)

        sign = re.findall(r'<dd data-field="predicate">标签</dd>.*?<dd data-field="object">(.*?)</dd>', html,re.S | re.M)
        # print(sign)

        describe = ','.join(describe)
        sign = ','.join(sign)
        #去掉大众关键字出来不要的新闻
        titles = re.findall(r'<title>(.*?) - Magi</title>',html)[0]
        if titles == '大众':

            title_lists = re.findall(r'<h3>(.*?)</h3>', html)
            # title_list = title_lists[3:]
            items['title'] = title_lists[3:]
            # items['title'] = ','.join(title_list)
            # items['title'] = title_list
            # 获取每个新闻标题的url
            link_lists = re.findall(r'<div class="card" data-type="web">[\s\S]<a href="(.*?)">', html)
            # link_list = link_lists[3:]
            items['url'] = link_lists[3:]
            # items['url'] = ','.join(link_list)
            # items['url'] = link_list
            # 获取每个新闻的内容描述
            contents_lists = re.findall(r'<div class="card" data-type="web">[\s\S]<a href=".*?">[\s\S]<h3>.*?</h3>[\s\S]<cite>.*?</cite>[\s\S]</a>[\s\S](.*?)[\s\S]</div>',html)
            items['infor'] = contents_lists
            # items['infor'] = ','.join(contents_list)
            # print(type(items['infor']))
            # print('(*(*(*(***************************')
        else:

            titles = re.findall(r'<h3>(.*?)</h3>', html)
            items['title'] = titles
            # items['title'] = ','.join(titles)
            # items['title'] = titles
            #获取每个新闻标题的url
            link_lists = re.findall(r'<div class="card" data-type="web">[\s\S]<a href="(.*?)">',html)
            items['url'] = link_lists
            # items['url'] = ','.join(link_lists)
            # items['url'] = link_lists
            #获取每个新闻的内容描述
            contents_lists = re.findall(r'<div class="card" data-type="web">[\s\S]<a href=".*?">[\s\S]<h3>.*?</h3>[\s\S]<cite>.*?</cite>[\s\S]</a>[\s\S](.*?)[\s\S]</div>',html)
            items['infor'] = contents_lists
            # items['infor'] = ','.join(contents_lists)
            # print(type(items['infor']))
            # print('(*(*(*(***************************')
        return describe,sign,items

    def to_oracle(self,describe,sign,items):
        new_item = {}
        update_item = {}
        new_item['CTYPE'] = BD_item['CTYPE']
        new_item['KEYWORD'] = BD_item['KEYWORD']
        new_item['BD_ID'] = BD_item['BD_ID']
        new_item['BRAND'] = BD_item['BRAND']
        new_item['PRICES'] = BD_item['PRICES']
        new_item['CAR_ID'] = BD_item['CAR_ID']
        new_item['GUOBIE'] = BD_item['DUOBIE']
        new_item['CAR_TYPE'] = BD_item['CAR_TYPE']
        new_item['CAR_LEVEL'] = BD_item['CAR_LEVRL']
        new_item['ENERGY'] = BD_item['ENERGY']

        new_item['DISCRIBE'] = describe
        new_item['SIGN'] = sign
        update_item['title'] = items['title']
        update_item['url'] = items['url']
        update_item['infor'] = items['infor']
        insert_ora = "insert into magi (CTYPE, KEYWORD, BD_ID,BRAND, PRICES, CAR_ID, GUOBIE, CAR_TYPE, CAR_LEVEL, ENERGY, DISCRIBE, SIGN) values (:CTYPE, :KEYWORD, :BD_ID,:BRAND, :PRICES, :CAR_ID, :GUOBIE, :CAR_TYPE, :CAR_LEVEL, :ENERGY, :DISCRIBE, :SIGN)"
        try:
            # cursor.execute(insert_ora)
            cursor.execute(insert_ora, new_item)
            # 4. 提交操作
            connect.commit()
            print('插入成功')
        except Exception as e:
            print('插入失败')
            print(e)

        #title,url,infor的list
        for title,url,infor in zip(update_item['title'],update_item['url'],update_item['infor']):
            # print(title,url,infor)
            print('8888888888888888888888888888888')
            insert_sql = "insert into magi_extend (CTYPE,KEYWORD,BD_ID,TITLE,URL,INFOR) values ('{}','{}','{}','{}','{}','{}')".format(new_item['CTYPE'],new_item['KEYWORD'],new_item['BD_ID'],title,url,infor)
            print(insert_sql)
            try:
                cursor.execute(insert_sql)
                connect.commit()
                print('插入magi_extend成功')
            except Exception as err:
                print('插入magi_extend失败')
                print(err)
    def close_bro(self):
        self.browser.close()

    def run(self,BD_item):
        # time.sleep(random.choice([1,2,3]))
        html = self.search_keyword(BD_item)
        describe,sign,items = self.parse_data(html)
        self.to_oracle(describe,sign,items)

if __name__ == '__main__':
    items=[]
    while True:

        # 网站爬虫
        while True:
            magispider = MagiSpider()
            for BD_item in baidu_item[i:]:
            # for BD_item in baidu_item:
                try:
                    magispider.run(BD_item)
                    # time.sleep(random.choice(1,1.5))
                except:
                    pass
                i += 1
                print(i)
                if i % 4 == 0:
                    magispider.close_bro()
                    break
                time.sleep(10)
        cursor.close()
        connect.close()

        # time.sleep(3600*24)






