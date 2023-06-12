# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

def get_cookies_dict():
    cookies_str = 'bid=5vHRxwzPfWk; ll="108288"; _ga=GA1.2.1031765219.1683755657; __utmc=30149280; __utmc=223695111; ' \
                  'trc_cookie_storage=taboola%2520global%253Auser-id%3D90dfdc74-9d30-4e84-a5ee-b5949643953d' \
                  '-tucta519b5c; _vwo_uuid_v2=DAEBF6C9130EC4B28E5ADAACD2E7C7E62|1f373ceedf3cc407298c22c17f2bc93a; ' \
                  '__utmz=30149280.1686496566.9.5.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(' \
                  'not%20provided); __utmz=223695111.1686496566.9.5.utmcsr=google|utmccn=(' \
                  'organic)|utmcmd=organic|utmctr=(not%20provided); dbcl2="213834581:qp0rJ+lnfTY"; ck=Lzeh; ' \
                  'push_noty_num=0; push_doumail_num=0; ' \
                  '__gads=ID=db4190d656932049-22e5a623cedc008d:T=1683755673:RT=1686497872:S=ALNI_MYJ0HKX3BeEcQ6f4et' \
                  '-WhVbc8bTlQ; __gpi=UID=00000bec5b2ec400:T=1683755673:RT=1686497872:S' \
                  '=ALNI_MYN8LVQeMJGyPFxSRbMHeuSn739Vw; ' \
                  '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1686500728%2C%22https%3A%2F%2Faccounts.douban.com%2F%22' \
                  '%5D; ap_v=0,6.0; __utma=30149280.1031765219.1683755657.1686496566.1686500745.10; ' \
                  '__utma=223695111.1031765219.1683755657.1686496566.1686500745.10; ' \
                  '_pk_id.100001.4cf6=cf10b52e64bbc0d1.1683755671..1686500853.undefined. '
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
        request.cookies = COOKIES
        # request.meta = {'proxy': 'socks5://127.0.0.1:10808'}
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
