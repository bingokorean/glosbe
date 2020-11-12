#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wen Oct 14 10:07:59 2020

@author: wanghao87

"""

import os
import sys
# import Tkinter as tk
# import tkMessageBox
from datetime import datetime
import codecs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def get_content(drive, url):
    # drive.implicitly_wait(3)
    drive.get(url)

    # block_content = WebDriverWait(drive,3).until(
    #     EC.presence_of_element_located((By.ID, "translationExamples"))
    # )

    try:
        block_content = drive.find_element_by_xpath('//*[@id="translationExamples"]')
        blocks_content = block_content.find_elements_by_class_name("nobold")

    except NoSuchElementException as e:
        drive.close()
        print e
        print "验证链接：", url
        # tkMessageBox.showwarning('Error','Please Verify! \n url: ' + url)
        os._exit(0)

    res_line = []
    res = []

    for i in range(len(blocks_content)):
        if i % 2 == 0:
            res_line = blocks_content[i].text
            continue
        else:
            res_line = res_line + '\t' + blocks_content[i].text
        # print res_line
        res.append(res_line)
    # print type(res)
    # print res
    if res:
        print "Get!"
    else:
        print "None!"
        return -1
    save(res, 'zhja.txt')

    res = []
    return 1

def get_zh():
    zh = pd.read_excel("most_frequent_chinese.xlsx", sheet_name=0)
    return zh['Character'].values

def get_zh2():
    words = []
    with open("word_ja.txt.u",'r') as f:
        for word in f:
            words.append(word.rstrip())
    # print words
    return words



def url_create(word, page):
    url_prefix = "https://glosbe.com/zh/ja/"
    # url_param = "?page=?&tmmode=MUST"

    # if page == 1:
    #     url = url_prefix + word
    #     # print "i=1",url
    #     return url
    # else:
    #     url = url_prefix + word + '?page=' + str(page) + '&tmmode=MUST'
    #     # print "i=1+",url
    #     return url
    url = url_prefix + word + '?page=' + str(page) + '&tmmode=MUST'
    return url


def login(drive, email, password):
    url = "https://auth2.glosbe.com/login?returnUrl=http%3A%2F%2Fglosbe.com%2FloginRedirectInternal"
    index = "https://glosbe.com/"
    drive.implicitly_wait(3)
    drive.get(url)

    if drive.current_url == index:
        return 1
    else:
        # input_email = 
        drive.find_element_by_xpath('//*[@id="username"]').send_keys(unicode(email, 'utf-8'))
        # input_password = 
        drive.find_element_by_xpath('//*[@id="password"]').send_keys(unicode(password, 'utf-8'))
        # login
        drive.find_element_by_xpath('//*[@id="fm1"]/div[2]/div/div[2]/button').click()

        if drive.current_url == "https://auth2.glosbe.com/login?error":
            print "login error"
            return -1
        else:
            return 1


def save(res, fileName):
    f = codecs.open(fileName, 'a+', 'utf-8')
    for each in res:
        f.write(each + '\n')
    f.close()


if __name__ == "__main__":

    start = sys.argv[1]
    # end = sys.argv[2]
    start = int(start)
    # end = int(end)
    words = get_zh2()
    words = words[start:]
    print words
    # print words[start]
    # os._exit(0)

    prefs = {
        'profile.default_content_settings': {
            'profile.default_content_setting_values': {
                'images': 2,  # 不加载图片
                'javascript': 2,  # 不加载JS
                # "User-Agent": ua, # 更换UA
            }}}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    drive = webdriver.Chrome(options=chrome_options)
    drive.maximize_window()

    
    if login(drive, email, password) == -1:
        print "login error!"
        drive.close()
        os._exit(0)
    # word = "%E8%BF%9B"
    # url = url_create(word)

    pages = 10

    time_list = []
    time_sum = 0

    time_program_start = datetime.now()

    for word in words:
        time_start = datetime.now()
        for page in range(4, pages):
            print word, ": 第", page, "页"
            url = url_create(word, page)
            # drive.get(url)
            # drive.implicitly_wait(3)
            flag = get_content(drive, url)
            if flag == -1:
                break
        time_end = datetime.now()
        diff = (time_end - time_start).seconds
        time_list.append(diff)
        print time_list
        time_sum = time_sum + diff
        print "字数:", len(time_list)
        print "总用时:", time_sum, "s"
        print "平均用时:", time_sum / len(time_list), "s"
        print "以上是第", start, "个字到结果"
        start = start + 1
        print "完成时间:", datetime.now()
    print "字数:", len(time_list)
    print "总用时:", time_sum, "s"
    print "平均用时:", time_sum / len(time_list), "s"
    print "程序开始执行时间", time_program_start
    print "程序完成执行时间", datetime.now()
    # cookie = drive.get_cookies()
    # for each in cookie :
    #     print each
    drive.close()
