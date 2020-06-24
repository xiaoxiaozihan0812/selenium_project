#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2020/6/15 13:30
# @Author   : zihan.zhao
# @File     : TestDemo.py
# @Software : PyCharm
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
import re
import time
import sys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pymysql
import tkinter as tk
from PIL import  Image,ImageEnhance
import threading
import pytesseract
import chaojiying

a=0
num = 0
num1 = 0
num2=0

def indexhtml(user,password):
    time.sleep(1)
    driver.get('http://zzx.ouchn.edu.cn/edu/public/student/#/login')
    time.sleep(1)
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_xpath('//input[@type="text"]').send_keys(user)
    driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)


def getcaptcha():
    element = driver.find_element_by_id("verifyCanvas")
    driver.save_screenshot(r'./screenshot.png')
    left = element.location['x']
    top = element.location['y']
    right = element.location['x'] + element.size['width']
    bottom = element.location['y'] + element.size['height']
    im = Image.open(r'./screenshot.png')
    im = im.crop((left, top, right, bottom))
    im.save(r'./screenshot.png')

def use_getcaptcha():
    im = open(r'./screenshot.png', 'rb').read()
    capt=chaojiying.PostPic(im, 4004)
    os.remove(r'./screenshot.png')
    captcha=capt['pic_str']
    return captcha

def login(captcha,user):
    driver.find_element_by_name('password').send_keys(str(captcha))
    driver.find_element_by_class_name('logC_btn').click()
    print('请等待此账号提示登录成功，提示成功后即可打开新的程序来登录新账号')
    lb.insert(tk.END, '请等待此账号提示登录成功，提示成功后即可打开新的程序来登录新账号')
    time.sleep(5)
    if len(driver.find_elements_by_xpath('//div[@class="title"]')) <3:
        print('WARNING:验证码识别错误，将自动重新识别')
        lb.insert(tk.END, 'WARNING:验证码识别错误，将自动重新识别')
        run()

    else:
        print('账号', user, '登录成功，开始学习')
        lb.insert(tk.END, '账号' + user + '登录成功，开始学习')
        startlearn(user)
def startlearn(user):
    time.sleep(2)

    if len(driver.find_elements_by_xpath('//div[@class="title"]'))>1:
        try:
            print('一共查询到有', str(len(driver.find_elements_by_xpath('//div[@class="title"]'))), '门课程')
            lb.insert(tk.END, '一共查询到有'+ str(len(driver.find_elements_by_xpath('//div[@class="title"]')))+'门课程',)
            for i in range(len(driver.find_elements_by_xpath('//div[@class="title"]'))):
                if '100' in driver.find_elements_by_xpath('//span[@class="jdb"]')[i].text:
                    print('第',str(i+1),'门课程',driver.find_elements_by_xpath('//div[@class="title"]')[i].text,'已经学完')
                    lb.insert(tk.END, '第'+str(i+1)+'门课程'+driver.find_elements_by_xpath('//div[@class="title"]')[i].text+'已经学完')
                else:
                    print('进入第' ,str(i + 1) ,'门课程' , driver.find_elements_by_xpath('//div[@class="title"]')[i].text)
                    lb.insert(tk.END, '进入第' +str(i + 1) +'门课程' + driver.find_elements_by_xpath('//div[@class="title"]')[i].text)
                    subject=driver.find_elements_by_xpath('//div[@class="title"]')[i].text
                    driver.find_elements_by_xpath('//div[@class="title"]')[i].click()
                    time.sleep(3)
                    if len(driver.find_elements_by_xpath('//li[@class="chapterItem"]'))>1:
                        for j in driver.find_elements_by_xpath('//li[@class="chapterItem"]'):
                            j.click()
                            time.sleep(1)

                        for k in range(len(driver.find_elements_by_xpath('//li[@class="setionItem"]'))):
                            print('开始学习第',str(i+1),'门课程',subject,'的第',str(k+1),'节课...')
                            lb.insert(tk.END, '开始学习第'+str(i+1)+'门课程'+subject+'的第'+str(k+1)+'节课...',)
                            if '100' in driver.find_elements_by_xpath('//span[@class="jdb"]')[k].text:
                                print('第',str(i+1),'门课程',subject,'的第',str(k+1),'节课','已经学完，开始学习下一小节')
                                lb.insert(tk.END, '第'+str(i+1)+'门课程'+subject+'的第'+str(k+1)+'节课'+'已经学完，开始学习下一小节')
                            else:
                                element=driver.find_elements_by_xpath('//li[@class="setionItem"]')[k]
                                driver.execute_script("arguments[0].click();", element)
                                answerquestion()
                                wait.until(EC.visibility_of_element_located((By.XPATH,'//div[@class="backbtn btn"]')))
                                time.sleep(5)
                                driver.find_element_by_xpath('//div[@class="backbtn btn"]').click()
                                time.sleep(5)
                                for j in driver.find_elements_by_xpath('//li[@class="chapterItem"]'):
                                    j.click()
                                    time.sleep(2)
                        driver.find_element_by_xpath('//li[@class="childActive"]').click()
                    else:
                        global num2
                        num2 += 1
                        if num2 == 10:
                            run()
                            num2 = 0
                        else:
                            print('WARNING:网络波动，页面长时间未能加载，正在尝试重新运行!!!')
                            lb.insert(tk.END, 'WARNING:网络波动，页面长时间未能加载，正在尝试重新运行!!!')
                            driver.get('http://zzx.ouchn.edu.cn/edu/public/student/#/courseList/1')
                            time.sleep(5)
                            startlearn(user)

            print(user,'学习结束')
            lb.insert(tk.END, user+'学习结束',)
            time.sleep(2)
            driver.quit()

        except:
            global num1
            num1+=0
            if num1==10:
                run()
                num1=0
            else:
                print('WARNING:网络波动，页面长时间未能加载，正在尝试重新运行!!!')
                lb.insert(tk.END, 'WARNING:网络波动，页面长时间未能加载，正在尝试重新运行!!!')
                driver.get('http://zzx.ouchn.edu.cn/edu/public/student/#/courseList/1')
                time.sleep(5)
                startlearn(user)
    else:
        global num
        num+=1
        if num==10:
            run()
            num=0
        else:
            print('WARNING:网络波动，页面长时间未能加载，正在尝试重新运行!!!')
            lb.insert(tk.END, 'WARNING:网络波动，页面长时间未能加载，正在尝试重新运行!!!')
            driver.get('http://zzx.ouchn.edu.cn/edu/public/student/#/courseList/1')
            time.sleep(5)
            startlearn(user)

def answerquestion():
    time.sleep(5)
    if len(driver.find_elements_by_xpath('//div[@class="see"]')) ==0:
        print('此课程无题')
        lb.insert(tk.END,'此课程无题')
        print('等待视频播放结束自动播放下节视频')
        lb.insert(tk.END, '等待视频播放结束自动播放下节视频')
    else:
        print('此课程有题，开始答题...')
        lb.insert(tk.END, '此课程有题，开始答题...')
        # print('查看正确答案')
        # lb.insert(tk.END, '查看正确答案')
        elements=driver.find_elements_by_xpath('//div[@class="see"]')
        for i in elements:
            i.click()

        print('正在自动选择正确答案...')
        lb.insert(tk.END, '正在自动选择正确答案...')
        time.sleep(2)
        for j in range(len(driver.find_elements_by_xpath('//div[@class="subject"]'))):
            answer=driver.find_elements_by_xpath('//div[@class="right_key"]//span')[j].text
            print(answer)
            lb.insert(tk.END, answer)
            time.sleep(1)
            if 'A' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[0].click()

            if 'B' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[1].click()

            if 'C' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[2].click()

            if 'D' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[3].click()

            if 'E' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[4].click()

            if 'F' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[5].click()

            if 'G' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[6].click()

            if 'H' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[7].click()

            if 'I' in answer:
                driver.find_elements_by_xpath('//div[@class="subject"]')[j].find_elements_by_xpath('.//div[@class="answer"]')[8].click()
            time.sleep(1)
        print('答题结束，等待学习视频播放完毕，自动学习下面的视频')
        lb.insert(tk.END, '答题结束，等待学习视频播放完毕，自动学习下面的视频')




def thread_it(func):
    '''将函数放入线程中执行'''
    # 创建线程
    t = threading.Thread(target=func)
    # 守护线程
    t.setDaemon(True)
    # 启动线程
    t.start()


def run():
    global a
    a+=1
    if a>=5:
        print('连续登陆五次失败，可能是网站崩溃或者验证码到期或者宽带断线，请检查后重启程序再试')
        lb.insert(tk.END, '连续登陆五次失败，可能是网站崩溃或者验证码到期或者宽带断线，请检查后重启程序再试')
    else:
        user = inputuser.get()
        user = ''.join(user.split())
        password = inputpassword.get()
        password = ''.join(password.split())
        print('请保持网络状态良好，同时登录多个账号观看视频，会占用电脑很大的带宽，不建议使用wifi，建议电脑连接网线，网络状态差会影响学习进度,')
        lb.insert(tk.END, '请保持网络状态良好，同时登录多个账号观看视频，会占用电脑很大的带宽，不建议使用wifi，建议电脑连接网线，网络状态差会影响学习进度,')
        indexhtml(user,password)
        getcaptcha()
        login(use_getcaptcha(),user)


if __name__ == '__main__':

    # 第1步，实例化object，建立窗口window
    window = tk.Tk()
    # 第2步，给窗口的可视化起名字
    window.title('Auto Study program - V1.2')
    window.geometry("700x800")
    labeluser = tk.Label(window, text="请输入账号")
    labeluser.pack()
    inputuser = tk.Entry(window, width=30)
    inputuser.pack()
    labelpassword = tk.Label(window, text="请输入密码")
    labelpassword.pack()
    inputpassword = tk.Entry(window, width=30)
    inputpassword.pack()
    btn = tk.Button(window, text='Login', command=lambda: thread_it(run))
    btn.pack()
    lb = tk.Listbox(window)
    scr = tk.Scrollbar(window)
    lb.config(yscrollcommand=scr.set)
    scr.config(command=lb.yview)
    lb.pack(side=tk.LEFT, expand=tk.YES,fill=tk.BOTH)
    scr.pack(side=tk.RIGHT, fill=tk.Y)
    chaojiying = chaojiying.Chaojiying_Client('xiaozihan0812', 'xiaozihan0812',
                                              '49fd6c3dac503e8410f71ab7e926285b')  # 用户中心>>软件ID 生成一个替换 96001  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//									#1902 验证码类型
    chrome_options = Options()
    # # 设置chrome浏览器无界面模式
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--mute-audio")
    # webdriver.Firefox(executable_path='.\Google\Chrome\Application\chrome.exe')
    driver = webdriver.Chrome(r'./settings/chromedriver.exe', chrome_options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(60)
    wait = WebDriverWait(driver, 3600, 0.5)
    window.mainloop()





