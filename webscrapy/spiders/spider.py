import scrapy
from scrapy import Request

from webscrapy.items import WebscrapyItem

class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["douban.com"]
    headers = {} #

    def start_requests(self):
        for page in range(1):
            yield Request(
                url=f'https://movie.douban.com/top250?start={page * 25}&filter=',
                # meta={'proxy':'socks5://127.0.0.1:10808'},
                # headers=self.headers
            )

    def parse(self, response, **kwargs):
        print(f"请求头信息为: {response.request.headers.get('User-Agent')}")

        li_list = response.xpath(r'//*[@id="content"]/div/div[@class="article"]/ol/li')

        for li in li_list:
            detailed_url = li.xpath('./div/div[@class="info"]/div[@class="hd"]/a/@href').get()
            item = WebscrapyItem()
            name = li.xpath(r'./div[@class="item"]/div[@class="info"]/div[@class="hd"]/a/span[1]/text()')[0].extract()
            rating = li.xpath(r'./div[@class="item"]/div[@class="info"]/div[@class="bd"]/div['
                              r'@class="star"]/span[@class="rating_num"]/text()')[0].extract()
            info = li.xpath(r'./div/div[2]/div[2]/p[2]/span/text()').extract() or ''  # some film does not have info
            item['name'] = name
            item['rating'] = rating
            item['info'] = info
            if len(info) == 0:
                item['info'] = 'blank content'
            else:
                item['info'] = info[0]
            yield Request(url=detailed_url, callback=self.parse_detail, cb_kwargs={'item': item})

    def parse_detail(self, response, **kwargs):
        item = kwargs['item']
        item['length'] = response.xpath('//*[@id="info"]/span[@property="v:runtime"]/@content')[0].extract()
        item['abstract'] = response.xpath('//span[@property="v:summary"]/text()')[0].extract()

        yield item

