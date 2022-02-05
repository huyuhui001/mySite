### File demo.py
Get video names and links and export to talks.txt and links.txt   
Using m3u8 to find out videos.
Using merge.bat to merge video segments into one video file

### File image_link.py
Get image names and links   

### File `SpiderVideo.py` to download video segments and consolidate into one video file
The file `SpiderVideo.py` reads from `index.m3u8` as input to download video segments.   
The file `index.m3u8` is maintained manually from target webpage.   
Destination folder: `/opt/projects/myPython/pythonSpider/video_download`    
Consolidation: `merge.bat`
Key is to get links of videos below:
```
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
```

### File SpiderImage.py to download images
Destination folder: `/opt/projects/myPython/pythonSpider/images_download`
Key is to get links below
```
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
```
