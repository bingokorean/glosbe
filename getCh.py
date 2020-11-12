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
if __name__ == "__main__":
    fileName = sys.argv[1]
    zh = pd.read_excel(fileName,sheet_name=0)
    word =  zh['Character'].values
    # word = word.encode("gb18030").decode("gb18030")
    print word
    a, b, c, d, e, f, g = np.hsplit(word,7)
    
    # for each in word:
    #     print each
        # print each.decode('')
        # print unicode(each, 'utf-8')
        # print each
        
        # print urllib.pathname2url(each)

        # request = requests.get(each)
        # print request.url


