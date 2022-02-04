#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import requests
import urllib
from urllib import request, error

url = 'http://www.cnblogs.com'
response = urllib.request.urlopen(url, timeout=0.1)  # 发送请求

try:
    if response.getcode() == 200:
        data = response.read()
        print(data.decode('UTF-8'))
except error.URLError as e:
    print(e.reason)
except Exception as e:
    print('error')
finally:
    print('done....')
