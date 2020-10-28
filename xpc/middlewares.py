# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from scrapy.exceptions import NotConfigured
import redis


class XpcSpiderMiddleware:
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class XpcDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
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
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.r = redis.Redis(host='127.0.0.1')
        self.proxy_key = settings.get('PROXY_REDIS_KEY')
        self.proxy_stats_key = self.proxy_key + "_stats"
        self.max_failed = 5

    @property
    def proxies(self):
        return [i.decode('utf-8') for i in self.r.lrange(self.proxy_key, 0, -1)]

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("HTTPPROXY_ENABLED"):
            raise NotConfigured
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if not request.meta.get('proxy') \
                and request.url not in spider.start_urls:
            request.meta['proxy'] = random.choice(self.proxies)

    def process_response(self, request, response, spider):
        cur_proxy = request.meta.get('proxy')
        if response.status in (401, 403):
            print('{} got wrong code {} times'.
                  format(cur_proxy, self.r.hget(self.proxy_stats_key, cur_proxy)))
            self.r.hincrby(self.proxy_stats_key, cur_proxy, 1)
        failed_times = self.r.hget(self.proxy_stats_key, cur_proxy) or 0
        if int(failed_times) >= self.max_failed:
            self.removeProxy(cur_proxy)
            del request.meta['proxy']
            print('got wrong http code [{}] when use {}'.format(
                response.status, cur_proxy))
            self.removeProxy(proxy=cur_proxy)
            del request.meta['proxy']
            return request
        return response

    def process_exception(self, request, exception, spider):
        cur_proxy = request
        from twisted.internet.error import ConnectionRefusedError, TimeoutError
        if isinstance(exception, (ConnectionRefusedError, TimeoutError)):
            print('error occur when use proxy {}'.format(exception))
            self.removeProxy(proxy=cur_proxy)
            del request.meta['proxy']
            return request

    def removeProxy(self, proxy):
        if proxy in self.proxies:
            self.r.lrem(self.proxy_key, proxy)
            self.r.hdel(self.proxy_stats_key, proxy)
            print('remove {} from proxy list'.format(proxy))
