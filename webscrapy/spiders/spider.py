"""
Project: Web scraping for customer reviews
Author: Hào Cui
Date: 06/12/2023
"""
import scrapy
from scrapy import Request

from webscrapy.items import WebscrapyItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["www.amazon.co.uk"]
    headers = {} #

    def start_requests(self):
        # keywords = ['DeWalt', 'Black+and+Decker', 'Stanley', 'Craftsman', 'Porter-Cable', 'Bostitch', 'Irwin+Tools',
        #             'Lenox']
        keywords = ['DeWalt']
        company = 'Stanley Black and Decker'

        # from search words to generate product_urls
        search_urls = []
        for keyword in keywords:
            search_urls = [f'https://www.amazon.co.uk/s?k={keyword}+{company.replace(" ", "+")}r&page={page}&qid=1686602870&ref=sr_pg_{page}' for page
                       in range(1,8)]

        # yield request of each product_url to scrapy
        for search in search_urls:
            yield Request(
                url=search,
                # meta={'proxy':'socks5://127.0.0.1:10110'},
                # headers=self.headers
            )

    def parse(self, response, **kwargs):
        product_urls = response.xpath('//*[@id="search"]//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]/@href').extract()

        for product_url in product_urls:
            product_url_detailed = f'https://www.amazon.co.uk/{product_url}'
            yield Request(url=product_url_detailed, callback=self.product_parse)


    def product_parse(self, response: Request, **kwargs):
        href = response.xpath('//a[@class="a-link-emphasis a-text-bold"]/@href').extract()
        if href:
            for each_href in href:
                product_reviews = f'https://www.amazon.co.uk/{each_href}'
                yield scrapy.Request(url=product_reviews, callback=self.review_parse)
        else:
            product = response.xpath('//*[@id="productTitle"]/text()').get()
            print(f'{product} has none of customer reviews')

    def review_parse(self, response: Request, **kwargs):
        review_list = response.xpath('//div[@id="cm_cr-review_list"]/div[@data-hook="review"]')
        for review in review_list:
            item = WebscrapyItem()
            item['product_name'] = response.xpath('//*[@id="cm_cr-product_info"]//a[@class="a-link-normal"]/text()')[-1].extract()
            item['customer_name'] = review.xpath('.//div[@class="a-profile-content"]/span/text()')[0].extract() or 'N/A'
            item['customer_rating'] = review.xpath('.//i/span[@class="a-icon-alt"]/text()')[0].extract() or 'N/A'
            item['customer_date'] = review.xpath('.//span[@data-hook="review-date"]/text()')[0].extract() or 'N/A'
            item['customer_review'] = review.xpath('.//span[@data-hook="review-body"]/span/text()').extract() or ['N/A']
            item['customer_support'] = review.xpath('.//span[@data-hook="helpful-vote-statement"]/text()').extract() or 'N/A'

            yield item

        # Generate the next page of customer reviews
        next_page_url = response.xpath('//li[@class="a-last"]/a/@href').get() or None
        if next_page_url:
            # print('success')
            next_page_url_full = f'https://www.amazon.co.uk/{next_page_url}'
            yield Request(url=next_page_url_full, callback=self.review_parse)
        else:
            # print('failure')
            pass


