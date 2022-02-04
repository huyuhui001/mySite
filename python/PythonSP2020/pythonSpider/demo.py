#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


class WebSpider(object):
    def __init__(self):
        self.url = 'https://www.ted.com/talks'
        self.talks = []
        self.links = []

    def get_html_text(self):
        response = requests.get(self.url)
        return response.text

    def get_talks_links(self):
        response = requests.get(self.url)
        html_text = response.text
        bs = BeautifulSoup(html_text, 'html.parser')
        results_div = bs.find('div', id='browse-results')
        results_div_h4 = results_div.find_all('h4', class_='f-w:700 h9 m5')
        # print(results_div_h4)
        for items in results_div_h4:
            self.talks.append(items.find('a').string)
            self.links.append(items.find('a').get('href') + '\n')

    def write_file(self, path, text):
        with open(path, mode='a', encoding='utf-8') as file:
            file.writelines(text)


if __name__ == '__main__':
    spider = WebSpider()
    # print(spider.get_html_text())

    spider.get_talks_links()
    print(spider.talks)
    print(spider.links)

    spider.write_file('links.txt', spider.links)
    spider.write_file('talks.txt', spider.talks)
