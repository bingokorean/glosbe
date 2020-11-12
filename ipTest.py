# -*- coding: utf-8 -*-

"""
Created on Sat Oct 10 17:41:59 2020

@author: wanghao87

"""
import urllib
import numpy as np
import requests
import pandas as pd
import sys


def get_ip():
    # http = "http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=&city=&port=1&format=txt&ss=3&css=&dt=1&specialTxt=3&specialJson=&usertype=2"
    http = "http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=1&time=1&pro=%E5%8C%97%E4%BA%AC%E7%9B%B4%E8%BE%96%E5%B8%82&city=%E5%8C%97%E4%BA%AC%E5%B8%82&port=1&format=txt&ss=3&css=&dt=1&specialTxt=3&specialJson=&usertype=2"
    request = requests.get(http)
    print request.text
    return request.text


if __name__ == "__main__":
    # target_url = "https://glosbe.com"
    target_url = "http://httpbin.org/ip"
    ip = get_ip()

    proxy_host = ip.split(":")[0]
    proxy_port = ip.split(":")[1]
    print proxy_host
    print proxy_port

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
        "https": proxys,
    }
    print proxies
    # r = requests.get(target_url)
    r = requests.get(target_url, proxies=proxies)
    #    each = '118.89.41.161'
    #    proxy_host = "http://" + each
    #    proxy = {
    #        "https": proxy_host
    #    }
    #    url = 'https://www.wwhhxhh.club/'
    #    res = urllib.urlopen(url,proxies=proxy).read()
    # print res
    #    print "success",res
    print r.status_code
    print r.text
