#!/usr/bin/env python 
# -*- coding:utf-8 -*-
"""
工作任务
(1)从给定的“http://127.0.0.1/02/school.html”页面中采集全国各省市高校名单列表。
(2)导入Python标准库urllib，通过HTTP/HTTPS协议自动从给定的互联网页面中获取数据并向其提交请求的方法；
(3)导入Python第三方库bs4、BeautifulSoup，从所爬取HTML页面中解析完整Web信息，采集全国高校列表及其链接；
(4)在屏幕上输出采集数据内容，如下所示：
    http://www.huaue.com/gx01.htm --->  北京普通高校名单
    http://www.huaue.com/gx02.htm --->  天津普通高校名单
    http://www.huaue.com/gx03.htm --->  河北普通高校名单
    ... ...
    http://www.huaue.com/gx34.htm --->  台湾高校名单
    http://www.huaue.com/gx35.htm --->  美国高校名单
"""

from bs4 import BeautifulSoup
from urllib import request

# url = 'http://127.0.0.1:81/02/school.html'
url = 'file:///C:/myProjects/myPython/pythonMyPractice/example/school.html'
response = request.urlopen(url)
html = response.read()
html = html.decode('utf-8')
soup = BeautifulSoup(html, "html.parser")
table2 = soup.find_all('table', id='table2')
td = table2[1].find_all('td')
for i in td:
    a = i.find_all('a')
    print(a[0].attrs['href'] + ' --->  ' + a[0].string)
