#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re  # regular expressions


class MySpiderBS4(object):
    def __init__(self):
        self.url = 'http://kb.cnblogs.com/'
        self.content = []

    def getContent(self):
        response = urllib.request.urlopen(self.url)
        htmlContent = response.read().decode('UTF-8')
        # soup = BeautifulSoup(htmlContent, "html.parser")
        # getHeadline = soup.find("div", attrs={"class": "list_block"})
        # getTargetItem = getHeadline.find_all("p", attrs={"target": "_blank"})

        for items in getTargetItem:
            self.content.append(items.text)


if __name__ == '__main__':
    mySpider = MySpiderBS4()
    mySpider.getContent()

    pattern = u'\((.*?)\)'  # u表示采用utf8的编码规则

    for i in mySpider.content:
        matchList = re.search(pattern, i)
        if matchList:
            print(i)
            print(matchList)
            print(matchList.group())
            print(matchList.group().split('/'))

'''
class MySpiderBS4(object):
    def __init__(self):
        self.url = 'http://www.cnblogs.com/'
        self.content = []

    def getContent(self):
        response = urllib.request.urlopen(self.url)
        htmlContent = response.read().decode('UTF-8')
        soup = BeautifulSoup(htmlContent, "html.parser")
        getHeadline = soup.find("div", attrs={"class": "card headline"})
        getTargetItem = getHeadline.find_all("a", attrs={"target": "_blank"})

        for items in getTargetItem:
             self.content.append(items.text)
'''

'''
************************Understand Attributes************************************************
editorPick = soup.find("a", attrs={"id": "editor_pick_lnk"})
print(editorPick)
print(editorPick['href'])
print(editorPick['id'])
print(editorPick['target'])
print(editorPick.attrs)
print(editorPick.text)
'''

'''
在解析html页面时无需关注注释，所以常见的做法是先判断类型，是NavigableString类型则再继续解析，如果是Comment类型，则可以直接丢弃
'''
"""
testHtmlContent = '''
<html>
    <head>
        <title>HTML Title</title>
    </head>
    <body>
        <p class='redColor'>Hello</p>
    </body>
</html>
'''
testSoup = BeautifulSoup(testHtmlContent, "html.parser")
print(testSoup.title)
'''
<title>HTML Title</title>
'''
print(testSoup.title.name)
'''
title
'''
print(testSoup.title.string)
'''
HTML Title
'''
print(testSoup.head)
'''
<head>
<title>HTML Title</title>
</head>
'''
print(testSoup.p)
'''
<p class="redColor">Hello</p>
'''
print(testSoup.p.name)
'''
p
'''
print(testSoup.p.attrs)
'''
{'class': ['redColor']}
'''
print(testSoup.p.attrs['class'])
'''
['redColor']
'''
"""
