import scrapy
from ..items import TedItem

# start the application with command below:
# scrapy crawl ted
'''
//*[@id="browse-results"]
//*[@id="browse-results"]/div[1]

//*[@id="browse-results"]/div[1]/div[1]
//*[@id="browse-results"]/div[1]/div[2]

//*[@id="browse-results"]/div[1]/div[@class="col"]
'''


class TedSpider(scrapy.Spider):
    name = 'ted'
    start_urls = ['https://www.ted.com/talks']

    def parse(self, response):
        # print(response.text)
        results = response.xpath('//*[@id="browse-results"]/div[1]/div[@class="col"]')
        # items = []

        for element in results:
            tedItem = TedItem()
            tedItem['talk'] = element.xpath('./div/div/div/div[2]/h4[2]/a/text()').extract_first()
            tedItem['link'] = element.xpath('./div/div/div/div[2]/h4[2]/a/@href').extract_first()
            # items.append((tedItem))
            yield tedItem  # pass tedItem to pipeline (item), which will be used as input from class MongoPipeline and JsonPipeline
        # return items
