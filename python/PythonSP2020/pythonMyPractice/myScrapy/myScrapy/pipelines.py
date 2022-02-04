# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# 在其中可以定义如何存储爬到的数据，可以是存入文件，也可以存入到数据库里


from itemadapter import ItemAdapter
import codecs
import json


class MyscrapyPipeline:
    def open_spider(self, spider):
        self.file = open('cnblog.json', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        json_string = json.dumps(dict(item)) + '\n'
        self.file.write(json_string)
        return item
