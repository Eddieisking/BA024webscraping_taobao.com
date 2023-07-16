"""
Project: Web scraping for customer reviews
Author: Hào Cui
Date: 07/04/2023
"""
import time

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils import create_chrome_driver, add_cookies
from webscrapy.items import WebscrapyItem


class SpiderSpider(scrapy.Spider):
    name = "spider"
    allowed_domains = ["taobao.com", "detail.tmall.com", "h5api.m.tmall.com", "s.taobao.com"]
    middleware = None

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.browser = None

    def start_requests(self):
        # keywords = ['DeWalt', 'Black+and+Decker', 'Stanley', 'Craftsman', 'Porter-Cable', 'Bostitch', 'Irwin+Tools',
        #             'Lenox']
        # company = 'Stanley Black and Decker'

        keywords = ['得伟官方旗舰店官网']
        """from search words to generate product_urls"""
        for keyword in keywords:
            for page in range(1):
                search_url = f'https://s.taobao.com/search?q={keyword}&s={page * 48}'
                yield self.selenium_request(url=search_url)

    def selenium_request(self, url):
        self.browser = create_chrome_driver(headless=False)
        self.browser.get('https://taobao.com')
        add_cookies(self.browser, 'taobao.json')
        self.browser.get(url)
        time.sleep(5)
        # Get the page source and create an HtmlResponse
        body = self.browser.page_source
        response = HtmlResponse(url=url, body=body, encoding='utf-8')

        # Create a new Request object based on the HtmlResponse
        request = Request(url=url, meta={'response': response}, callback=self.parse)
        request.meta['dont_filter'] = True  # Set the dont_filter attribute

        return request

    def parse(self, response, **kwargs):
        html_response = response.meta['response']
        selector = Selector(response=html_response)
        product_list = selector.xpath('//div[@class="m-itemlist"]//div[@class="items"]/div')

        review_list = []
        for product in product_list:
            try:
                product_url = f'https:' + product.xpath('.//div[@class="row row-2 title"]/a/@href')[0].extract()

                if 'detail.tmall.com' in product_url:
                    review_list.append(product_url)
                    yield from self.selenium_request_new(url=product_url)
            except:
                pass
        # start_url = 'https://taobao.com'

        # yield from self.selenium_request_new(review_list=review_list)  # Use yield from to delegate the generator

    def selenium_request_new(self, url):
        """Click the customer review button"""
        review_url = url
        # self.browser = create_chrome_driver(headless=False)
        # self.browser.get('https://taobao.com')
        # add_cookies(self.browser, 'taobao.json')
        self.browser.get(review_url)
        """Slider Validation"""
        comment_button = self.browser.find_element(By.XPATH,
                                                   '//div[@class="Tabs--title--1Ov7S5f "]')
        comment_button.click()
        time.sleep(5)

        """Pass the first page of response to scrapy to parse"""
        # Get the page source and create an HtmlResponse
        body = self.browser.page_source
        response = HtmlResponse(url=review_url, body=body, encoding='utf-8')

        # Create a new Request object based on the HtmlResponse
        request = Request(url=review_url, meta={'response': response}, callback=self.customer_review_parse,
                          dont_filter=True)

        yield request

        """Click the next page of customer review button"""
        while True:
            # Find the next button and store its reference
            try:
                next_button = self.browser.find_element(By.XPATH,
                                                        '//button[@class="detail-btn Comments--nextBtn--1itIAip"]')

                # Click the next button
                next_button.click()
                time.sleep(2)
            except:
                break

            """Pass the loaded response to scrapy to parse"""
            # Get the page source and create an HtmlResponse
            body = self.browser.page_source
            response = HtmlResponse(url=review_url, body=body, encoding='utf-8')

            # Create a new Request object based on the HtmlResponse
            request = Request(url=review_url, meta={'response': response}, callback=self.customer_review_parse,
                              dont_filter=True)

            yield request

            # Re-locate the next button element after the page refreshes
            try:
                next_button_new = self.browser.find_element(By.XPATH, '//button[@class="detail-btn Comments--nextBtn--1itIAip"]')
            except:
                print('No next_button_new')
                # self.browser.quit()
                break
                # WebDriverWait(self.browser, 10).until(
                # EC.presence_of_element_located(
                #     (By.XPATH, '//button[@class="detail-btn Comments--nextBtn--1itIAip"]')))

            time.sleep(2)
            print('Continue to the next page')

    def customer_review_parse(self, response, **kwargs):
        html_response = response.meta['response']
        selector = Selector(response=html_response)

        review_list = selector.xpath('//div[@class="Comments--comments--1662-Lt"]/div')

        for review in review_list:
            item = WebscrapyItem()
            item['product_name'] = selector.xpath('//div[@class="ItemHeader--root--DXhqHxP"]/h1/text()')[0].extract() or 'N/A'
            item['customer_name'] = review.xpath('.//div[@class="Comment--userName--2cONG4D"]/text()')[0].extract()
            item['customer_date'] = review.xpath('.//div[@class="Comment--meta--1MFXGJ1"]/text()')[0].extract() or 'N/A'
            item['customer_review'] = review.xpath('.//div[@class="Comment--content--15w7fKj"]/text()')[0].extract() or 'N/A'
            item['customer_support'] = review.xpath('.//div[@class="Comment--like--1swbsLo "]/button/span/text()')[0].extract() or 'N/A'
            # item['customer_browse'] = review.xpath('.//div[@class="Comment--visited--2t0QSw-"]/text()')[0].extract() or 'N/A'

            yield item

