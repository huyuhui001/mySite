#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from contextlib import closing
import os
import sys

class SpiderImage(object):
    def __init__(self):
        self.url = 'https://www.ted.com/talks'
        self.image_links = []

    def get_image_link(self):
        response = requests.get(self.url)
        html_text = response.text
        bs = BeautifulSoup(html_text, 'html.parser')
        results_div = bs.find('div', id='browse-results')

        # 方法1 （二选一即可）
        # results_div_span = results_div.find_all('span', class_='thumb__tugger')
        # for items in results_div_span:
        #     self.image_links.append(items.find('img').get('src') + '\n')

        # 方法2 （二选一即可）
        results_div_img = results_div.find_all('img')
        for items1 in results_div_img:
            self.image_links.append(items1.get('src') + '\n')

    def write_file(self, path, text):
        with open(path, mode='a', encoding='utf-8') as file:
            file.writelines(text)

    def download_image(self, path, image_url, filename):
        image_path = os.path.join(path, filename)
        request_headers = {'Accept': '*/*',
                           'Accept-Encoding': 'gzip, deflate, br',
                           'Accept-Language': 'zh-CN,zh;q=0.9',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        size = 0
        with closing(requests.get(image_url, headers=request_headers, stream=True)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])
            if response.status_code == 200:
                sys.stdout.write(filename + ' downloading...\n')
                sys.stdout.write('File Size: %0.2f MB\n' % (content_size / chunk_size / 1024))

                with open(image_path, 'wb') as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        sys.stdout.write('In Progress: %.2f%%' % float(size / content_size * 100) + '\r')
                        sys.stdout.flush()

    def start_download(self, links):
        for link in links:
            temp = link.split('/')[-1]
            filename = temp.split('?')[-2]
            self.download_image('/opt/projects/myPython/pythonSpider/images_download/', link, filename)


if __name__ == '__main__':
    spider = SpiderImage()
    spider.get_image_link()
    print(spider.image_links)
    spider.write_file('image_link.txt', spider.image_links)
    spider.start_download(spider.image_links)
