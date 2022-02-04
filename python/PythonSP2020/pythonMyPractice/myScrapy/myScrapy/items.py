# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# 在其中可以定义待爬取内容的数据结构

import scrapy


class MyscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 文章标题
    classify = scrapy.Field()  # 文章分类
    readNum = scrapy.Field()  # 文章阅读数
