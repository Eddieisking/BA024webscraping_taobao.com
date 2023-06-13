# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import random
from webscrapy.settings import USER_AGENT_LIST

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = 'session-id=262-5810110-4651945; ubid-acbuk=257-6978771-9482927; ' \
                  'x-acbuk="DhqB6Vxx@39xZAJgVE5hSsCCo@JcvyppwGxScJ2l?DHQGOY49AyksPPeXJbmJD4E"; ' \
                  'at-acbuk=Atza|IwEBIOiD2MyRQKSQeQgC9K-JIb9jjkwAUoChhdemoZ_xO1bg2W6fNGIF2cStoo0Z1O8T8IWm_erF3b4O' \
                  '-RclBW3_La55ALvWrPkxB8I7TtVw6HisoWCsFuUIJQNUvrx-ZXN197' \
                  '-5D5xy_yr9YMdyfBz_3WbM3yrpaLNjFYUYT4abn5H7CGOwos8egkv6h0zuSQwsJoqjlEf7n7TNYEEyTOyXvHkgl7y9r9ZLso21ajoYl2V_oA; sess-at-acbuk="avDIOAaEqIjYrKVnrekdr+sRMFSMiI3rW+8smTK58Wo="; sst-acbuk=Sst1|PQH2YDOsC7kmM3W17Uer2vA_CVZC-cctL420ehA28GXNTEQEzDY16LSTGuOhpg7FadGPKp4_-mh5iyJbgfZgdTqPTqGWc6orB1ANKW8MILxooyvrVSwqBU7gkCqaZc1VptkInAe2OCEq6Ktj0JlF19ZOAkSASGsNJTwDy1nQBXSaCWX93PIC_Ry_olQ1NLdYhhmZDi5m2ejQMoV2CkN5KJ0LOPtA_f5Unri1efL3PF-EivPbYV01PLDjHKwnk_FrVQK_M7ghkcMS5QDvb9lYK0-OFLV2uCAGqPuG6zIhnX33D50; lc-acbuk=en_GB; i18n-prefs=GBP; av-timezone=Europe/London; session-id-time=2082787201l; session-token=7AagOEW7Y5mhq2oaAFh96nJBHJGMukAV2OYd3wDC37mPb6N9IiHZOcu61yGE4PTifGy8R1Ii/pM6bXZstJYrizgDNRNffzvknuphsEbuns880C4yPaRCNReQZTxY4gwGu9WSIAAIDW9s9hv/rY1c2GH6qDHoNMc60t8+emmcDU/iljeN07ITgtCm5Io+FsWIk5fVIfMjLYufbD86rmAEz1SvHavEs/Ja8M6V4cBOaoAzsu+X3aI3gq2kQqEIN6QPxGzXPjdui4E=; csm-hit=tb:s-G0HC2MA54TBQNTQTDW50|1686648223378&t:1686648225738&adb:adblk_no '
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
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

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
        ua = random.choice(USER_AGENT_LIST)
        request.headers['User-Agent'] = ua

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
