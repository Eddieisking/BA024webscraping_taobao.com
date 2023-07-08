# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals, Request
import random
from selenium.webdriver.common.by import By

from scrapy.http import HtmlResponse
from selenium.common.exceptions import NoSuchElementException

from utils import create_chrome_driver, add_cookies
from webscrapy.settings import USER_AGENT_LIST
from scrapy.exceptions import IgnoreRequest, NotConfigured
import logging


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = 'thw=xx; t=905d11a40b9a0de6d81f56c057edf4e0; hng=GLOBAL%7Czh-CN%7CUSD%7C999; ' \
                  'cna=pqsZHdMvCjgCAYHqAKtK5hw6; _gid=GA1.2.1538006377.1688744321; ' \
                  '_m_h5_tk=03303be79014476695ed95b207ab02d6_1688753681366; ' \
                  '_m_h5_tk_enc=b1bad9a68b6332fbc24b21b22e27d3bf; xlly_s=1; cookie2=157ce1285065e2a4192780f4c3a03af9; ' \
                  '_tb_token_=73903e376791b; _samesite_flag_=true; alitrackid=world.taobao.com; ' \
                  'lastalitrackid=world.taobao.com; ' \
                  'sgcookie=E100Pc5yfLkManFEAnn1z9ixqh20S78GPJwW2dJOBvWCCi9edcA' \
                  '%2BQgmZpQRqlU0CX3EMGNxvhGEsziwBpCmvsXn2L0yWYbe6oSPDLzvyNWzEQX%2FM3mKLC9%2B3rTNKeJWenEk6; ' \
                  'unb=3992931653; uc1=cookie21=URm48syIYn73&cookie14=Uoe8gqe85VQ2sA%3D%3D&cookie15=UtASsssmOIJ0bQ%3D' \
                  '%3D&pas=0&existShop=false&cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D; ' \
                  'uc3=lg2=Vq8l%2BKCLz3%2F65A%3D%3D&id2=UNk%2Bf7g1WFFmzQ%3D%3D&vt3=F8dCsGIJ0ba0LVRSsT0%3D&nk2' \
                  '=F5RMGyOjhi5UaxU%3D; csg=3279b3cd; lgc=tb920300083; cancelledSubSites=empty; ' \
                  'cookie17=UNk%2Bf7g1WFFmzQ%3D%3D; dnk=tb920300083; skt=4cad3ac02e2944b9; ' \
                  'existShop=MTY4ODc0NDQ0OA%3D%3D; ' \
                  'uc4=nk4=0%40FY4HXgnfncfxpx9w4V1ufY3KwhRIMw%3D%3D&id4=0%40Ug40foE3DS9w50zCwzaHQDXdYAI%2F; ' \
                  'tracknick=tb920300083; _cc_=UtASsssmfA%3D%3D; _l_g_=Ug%3D%3D; sg=33a; _nk_=tb920300083; ' \
                  'cookie1=W8GLs2QPn6Dpd2sg7XuFTsY10SfHyzwtNdT%2BJ1HVBnE%3D; ' \
                  '_uetsid=5906c7e01cdc11ee9ee69730a376039c; _uetvid=f20724b0101211eeb6b06b52270ae4c4; ' \
                  '_ga=GA1.2.1111595517.1687338405; _ga_YFVFB9JLVB=GS1.1.1688744320.2.1.1688744949.0.0.0; ' \
                  'JSESSIONID=F74ED308F917BFFA63DE747CA5937D38; ' \
                  'isg=BDs7zMAg2-oNrudkoI8bXS-kyhmlkE-ShZHWoS35SjpjjFlutWAF4-UFpjzCrKeK; ' \
                  'l=fBjg_8LrNpmyxD_GBO5aourza77OaIObzsPzaNbMiIEGa1yh9IxumNC1X9LkWdtj3T5XbetPl_pr6dnWJRzU5skDBeYBRs5mpeJwReOmrtHl.; tfstk=cNwdB9NS7GKp8qQoQvCGUAM2YAjGa4ftzBgDeJZsXUvNZNTWysvTn-K-dMiju2IO. '
    cookies_dict = {}
    for item in cookies_str.split('; '):
        key, value = item.split('=', maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict


COOKIES = get_cookies_dict()


class WebscrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class WebscrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # def __init__(self):
    #     self.browser = create_chrome_driver(headless=False)
    #     self.browser.get('https://taobao.com')
    #     add_cookies(self.browser, 'taobao.json')

    # def __del__(self):
    #     self.browser.close()

    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # request.cookies = COOKIES
        # request.meta = {'proxy': 'socks5://127.0.0.1:10808'}
        # ua = random.choice(USER_AGENT_LIST)
        # request.headers['User-Agent'] = ua
        # # self.browser.implicitly_wait(5)
        # self.browser.get(request.url)
        #
        # try:
        #     comment_button = self.browser.find_element(By.XPATH,
        #                                                '//div[@class="Tabs--title--1Ov7S5f "]')
        #     comment_button.click()
        #     time.sleep(5)
        # except NoSuchElementException:
        #     pass
        #
        # return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8')

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class RotateProxyMiddleware:
    def __init__(self, proxies_file):
        self.proxies_file = proxies_file
        self.proxies = self.load_proxies()
        self.current_proxy = None

    @classmethod
    def from_crawler(cls, crawler):
        proxies_file = crawler.settings.get('PROXIES_FILE')
        return cls(proxies_file)

    def load_proxies(self):
        with open(self.proxies_file, 'r') as file:
            proxies = file.read().splitlines()
        return proxies

    def process_request(self, request, spider):
        if not self.current_proxy:
            self.current_proxy = self.get_random_proxy()

        request.meta['proxy'] = self.current_proxy
        print('current_proxy')
        print(self.current_proxy)

    def process_response(self, request, response, spider):
        if response.status == 403:
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request
        elif response.status == 307:
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, IgnoreRequest):
            # Handle IgnoreRequest exceptions
            if getattr(exception, 'response', None) is not None:
                return self.process_response(request, exception.response, spider)
            else:
                # IgnoreRequest without a response, re-raise the exception
                raise exception
        elif isinstance(exception, NotConfigured):
            # NotConfigured exception, re-raise it
            raise exception
        else:
            # Handle other exceptions
            self.remove_current_proxy()
            self.current_proxy = self.get_random_proxy()
            new_request = request.copy()
            new_request.dont_filter = True  # Disable duplicate request filtering
            return new_request

    def get_random_proxy(self):
        if not self.proxies:
            self.proxies = self.load_proxies()  # Reload proxies from the file if the list is empty
        return random.choice(self.proxies)

    def remove_current_proxy(self):
        if self.current_proxy in self.proxies:
            self.proxies.remove(self.current_proxy)