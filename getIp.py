# -*- coding: utf-8 -*- 
"""
Created on Mon Oct 12 11:01:59 2020

@author: wanghao87

"""

import random
import codecs
import urllib
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}
url = "http://m.feizhuip.com/Index/article/id/1133.html"
def get_ip_list(url):
    web_ip = requests.get(url,headers)
    soup = BeautifulSoup(web_ip.text,'lxml')
    tr = soup.select('tbody > tr')
    ip_list = []
    for each in tr:
        # print each.text
        # break
        ip = each.find('td')
        # print ip.text

        ip_list.append(ip.text.strip())
    # print ip_list
    for each in ip_list:
        try:
            proxy_host = "https://" + each
            proxy = {
                "https": proxy_host
            }
            url = 'https://www.baidu.com/'
            urllib.urlopen(url,proxies=proxy).read()
            # print res
            print "success",each
        except:
            ip_list.remove(each)
            print "fail",each
            continue
    return ip_list
# body > div.newsContianer > div.news-con > div > table > tbody > tr:nth-child(1) > td:nth-child(1)
if __name__ == "__main__":
    ip_list = get_ip_list(url)
    print ip_list
      
    f = codecs.open('ip_list.txt','w','utf-8')
    for each in ip_list:
        f.write(each + '\n')
    f.close()

