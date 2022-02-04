#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import scrapy
from myScrapy.items import MyscrapyItem


class BlogSpider(scrapy.Spider):
    name = 'cnblog'
    domain = ['kb.cnblogs.com']
    url = 'https://kb.cnblogs.com/'

    def parse(self, response):
        results = response.xpath('//*[@id="wrapper"]/div[4]/div/div[2]')
        items = []

        for elements in results:
            myItem = MyscrapyItem()
            myItem.title = elements.xpath('./div/div/div/p/a/text()').extract_first()
            myItem.classify = elements.xpath('./div/div/div/p/span/class()').extract_first()
            myItem.readNum = elements.xpath('./div/div/div[3]/p/span/class()').extract_first()
            yield myItem
        # items.append(myItem)
        # return items
