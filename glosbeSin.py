# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:01:59 2020

@author: wanghao87
"""
import os
import sys
import time
import random
from datetime import datetime
import codecs
import pandas as pd
import urllib
import requests
from requests.exceptions import RequestException
from requests.adapters import HTTPAdapter
import lxml
from bs4 import BeautifulSoup


def request_web(word, i):
    headerlist = [
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (X11; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;  Trident/5.0)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Mozilla/5.0 (iPad; CPU OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 Mobile/14B100 Safari/602.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    ]
    header = {}
    header["user-agent"] = headerlist[random.randint(0, len(headerlist) - 1)]

    cookie = {
        "cookie": "aFHoByEiQf3HaiyVsQizhw1dL1r7zhcA3ZRgSxMHFN3OXNefNoSK3tHS5TTR2VEXu2wEHodaciJidxCwoLhDHfebB2hr6n7lLp706hIi8yaP2yRzv8qX9nyXDXVMJeMYvSSRvlqw5Ua11HmupmmrUmpwSfAF"

    }

    link = 'https://glosbe.com/zh/ja/'
    if i == 1:
        url = link + word
    else:
        url = link + word + '?page=' + str(i) + '&tmmode=MUST'

    result = []

    try:
        result = get_content(url, header, cookie)
    except RequestException as e:
        print url
        print e
        save_word(word, "fail_word_ja_2.txt")
        print "连接目标网址失败,requests没有获取到数据"
        return -1

    if result:
        print "Get!"
        save(result, "zhja.txt")
        return 1
    else:
        print "None!"
        return 0


def get_content(url, header, cookie):
    session = requests.Session()
    session.mount('http://', HTTPAdapter(max_retries=10))
    session.mount('https://', HTTPAdapter(max_retries=10))

    print time.strftime('%Y-%m-%d %H:%M:%S')
    r = requests.get(url, headers=header, cookies=cookie, timeout=10)
    # r.raise_for_status()
    r.encoding = 'utf-8'

    res_list = []
    soup = BeautifulSoup(r.text, features="lxml")
    blocks = soup.find_all(class_="tableRow row-fluid")

    for each in blocks:
        content = each.find_all(class_="nobold")

        res = content[0].text + "\t" + content[1].text
        # print res

        res_list.append(res)
    return res_list


def get_proxy_ip():
    http = "http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=7&fa=1&fetch_key" \
           "=&groupid=0&qty=1&time=1&pro=%E5%8C%97%E4%BA%AC%E7%9B%B4%E8%BE%96%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8" \
           "%82&port=1&format=txt&ss=3&css=&dt=1&specialTxt=3&specialJson=&usertype=2 "
    request = requests.get(http)
    # print request.text
    return request.text


def get_proxy():
    ip = get_proxy_ip()
    proxy_host = ip.split(":")[0]
    proxy_port = ip.split(":")[1]
    # print proxy_host
    # print proxy_port

    proxy = "http://%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
    }
    proxys = "https://%(host)s:%(port)s" % {
        "host": proxy_host,
        "port": proxy_port,
    }
    proxies = {
        "http": proxy,
        "https": proxys
    }
    print proxies
    return proxies


def save_word(res, fileName):
    f = codecs.open(fileName, 'a+')
    f.write(res + '\n')
    f.close()


def save(res, fileName):
    f = codecs.open(fileName, 'a+', 'utf-8')
    for each in res:
        f.write(each + '\n')
    f.close()


def get_zh():
    zh = pd.read_excel("most_frequent_chinese.xlsx", sheet_name=0)
    return zh['Character'].values


def get_zh2():
    words = []
    with open("fail_word_ja.txt.u",'r') as f:
        for word in f:
            words.append(word.rstrip())
    # print words
    return words

if __name__ == "__main__":

    start = sys.argv[1]
    start = int(start)

    words = get_zh2()
    words = words[start:]

    timeList = []
    timeSum = 0

    page = 4

    for one in words:
        timeStart = datetime.now()
        cnt = 0
        # proxies = get_proxy()
        for i in range(1, page):
            print "page:", i
            print one

            res = request_web(one, i)
            if res == 0:
                break
            if res == -1:
                count = 0
                while True:
                    print "retry!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    print """
                    
                    #                       _oo0oo_
                    #                      o8888888o
                    #                      88" . "88
                    #                      (| -_- |)
                    #                      0\  =  /0
                    #                    ___/`---'\___
                    #                  .' \\\\|     |// '.
                    #                 / \\\\|||  :  |||// \\
                    #                / _||||| -:- |||||- \\
                    #               |   | \\\\\  -  /// |   |
                    #               | \_|  ''\---/''  |_/ |
                    #               \  .-\__  '-'  ___/-. /
                    #             ___'. .'  /--.--\  `. .'___
                    #          ."" '<  `.___\_<|>_/___.' >' "".
                    #         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
                    #         \  \ `_.   \_ __\ /__ _/   .-` /  /
                    #     =====`-.____`.___ \_____/___.-`___.-'=====
                    #                       `=---='
                    #
                    #
                    #     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    #
                    #               佛祖保佑         永无BUG
                    #
                    """
                    retry_res = request_web(one, i)
                    count = count + 1
                    print "第", count, "次尝试"
                    # if count >= 5:
                    #     proxies = get_proxy()
                    if retry_res != -1:
                        res = retry_res
                        break
            cnt = cnt + res

        print cnt, "页有数据"
        if cnt == 3:
            print one
            save_word(one, "word_ja.txt")

        timeEnd = datetime.now()
        diff = (timeEnd - timeStart).seconds
        timeList.append(diff)
        print timeList
        timeSum = timeSum + diff

        start = start + 1
        print "下面是第" + str(start) + "个字的结果"
    print timeSum / len(timeList)
