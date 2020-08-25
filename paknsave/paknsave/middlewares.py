# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import requests
import json


# class SimpleProxyMiddleware(object):
#     # 声明一个数组
#     proxyList = []
#
#     # Downloader Middleware的核心方法，只有实现了其中一个或多个方法才算自定义了一个Downloader Middleware
#     def process_request(self, request, spider):
#         # 随机从其中选择一个，并去除左右两边空格
#         proxy = random.choice(self.proxyList).strip()
#         # 打印结果出来观察
#         print("this is request ip:" + proxy)
#         # 设置request的proxy属性的内容为代理ip
#         request.meta['proxy'] = proxy
#
#     # Downloader Middleware的核心方法，只有实现了其中一个或多个方法才算自定义了一个Downloader Middleware
#     def process_response(self, request, response, spider):
#         # 请求失败不等于200
#         if response.status != 200:
#             # 重新选择一个代理ip
#             proxy = random.choice(self.proxyList).strip()
#             print("this is response ip:" + proxy)
#             # 设置新的代理ip内容
#             request.mete['proxy'] = proxy
#             return request
#         return response
#
#
class XunProxyMiddleware(object):
    """
    讯代理：http://www.xdaili.cn/
    注意：这是一次请求10个IP
    """

    # ==============代理初始化============
    def __init__(self):
        # 代理API
        # self.get_url = "http://daili.spbeen.com/get_api_json/?token=4nZufMcvqklMfwNjmiIXSseJ&num=10"
        self.get_url = "http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=3ba444e6ac6d4b8e8e76b373751f465b&orderno=YZ20208172449HUZH0H&returnType=2&count=10"
        # 测试地址
        self.teep_url = "https://www.baidu.com/"
        # IP代理池
        self.ip_list = []
        # 获取代理IP数量
        self.num = 10  # 修改获取IP数量
        # 用来记录使用IP的个数
        self.count = 0
        # 用来记录每个IP的使用次数
        self.evecount = 0


    # ==============获取代理IP============
    def getIPData(self):
        teep_data = requests.get(url=self.get_url).text
        self.ip_list.clear()
        for eve_ip in json.loads(teep_data)["RESULT"]:
            self.ip_list.append(
                {"ip":eve_ip,"port":eve_ip["port"]}
            )


    # ============改变原程序IP===========
    def changeProxy(self,request):
        ip = self.ip_list[self.count-1]["ip"]
        port = self.ip_list[self.count-1]["port"]
        request.meta["proxy"] = "http://" + str(ip) + ":" + str(port)


    # ==============验证代理IP============
    def verification(self):
        ip = self.ip_list[self.count - 1]["ip"]
        port = self.ip_list[self.count - 1]["port"]

        # 验证代理IP是否可用，并设置超时为5秒
        requests.get(url=self.teep_url,proxies={"http":str(ip) + ":" + str(port)},timeout=5)


    # ==============切换代理IP============
    def ifUsed(self,request):
        # 处理代理IP不可用的异常
        try:
            self.changeProxy(request)
            self.verification()
        except:
            if self.count == 0 or self.count == self.num:
                self.getIPData()
                self.count = self.count + 1
            else:
                self.count = self.count + 1
                self.ifUsed(request)


    def process_request(self,spider,request):
        if self.count == 0 or self.count ==self.num:
            self.getIPData()         # 获取代理IP信息
            self.count = 1

        # 判断代理IP使用次数
        if self.evecount == 3:       # 表示代理IP使用了几次
            self.count = self.count + 1
            self.evecount = 0
        else:
            self.evecount = self.evecount + 1
        self.ifUsed(request)        # 切换代理IP


class PaknsaveSpiderMiddleware:
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
        spider.logger.info('Spider opened: %s' % spider.name)


# class PaknsaveDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
