# -*- coding: utf-8 -*- 
import os
from selenium import webdriver
import requests
chromeOptions = webdriver.ChromeOptions()
ip = []
url = 'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=10&time=1&pro=&city=&port=1&format=txt&ss=3&css=&dt=1&specialTxt=3&specialJson=&usertype=2'

r = requests.get(url)
ip = r.text
ip_list = ip.splitlines()
print ip_list[0]
# os._exit(0)
# 设置代理
# chromeOptions.add_argument("--proxy-server=http://118.24.90.160:1080")
print ip[1]
chromeOptions.add_argument("--proxy-server=http://"+ip_list[0])
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(chrome_options = chromeOptions)

# 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
print browser.page_source 

# 退出，清除浏览器缓存
browser.quit()