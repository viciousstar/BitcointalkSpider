import re
import time
import os
from datetime import datetime
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy import log
from scrapy import signals
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError

from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message
from scrapy.xlib.tx import ResponseFailed
from BitcointalkSpider.util import incAttr
from BitcointalkSpider.settings import SPIDER_PRO_DIR

class MyRetryMiddleware(RetryMiddleware):
    """docstring for MyRetryMiddleware"""
    def __init__(self, settings):
        super(MyRetryMiddleware, self).__init__(settings)
        self.max_retry_main_times = settings.getint('RETRY_MAIN_TIMES')
        self.path = settings.get('SPIDER_RETRYURL_DIR')
        self.status = {self.genKey() : 0}
        self.maxExceptionTime = settings.getint('MAX_EXCEPTION_PER_HOUR')
        self.suspendTime = settings.getint('SUSPEND_TIME')
    @classmethod
    def from_crawler(cls, crawler):
        rt = cls(crawler.settings)
        crawler.signals.connect(rt.spider_opened, signal = signals.spider_opened)
        crawler.signals.connect(rt.spider_closed, signal = signals.spider_closed)
        return rt
    
    def genKey(self):
        return str(datetime.today().day) + str(datetime.today().hour)

    def spider_opened(self):
        try:
            self.file = open(self.path, 'a+')
        except:
            log.msg("Can not open retryUrl file in %s" %self.path, level = log.ERROR)
            self.file = None
    
    def spider_closed(self):       
        f = open(os.path.join(SPIDER_PRO_DIR, 'stat.info'), 'w+')
        f.writelines((str(self.status))
        self.file.close() if self.file else None

    def process_response(self, request, response, spider):
        if 'dont_retry' in request.meta:
            return response
        if response.status in self.retry_http_codes:
            #recode exception time and suspend spider
            key = self.genKey()
            incAttr(self.status, key)
            if self.status[key] >= self.maxExceptionTime:
                time.sleep(self.suspendTime)
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response
    
    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        url = request.url
        maxtimes = self.max_retry_main_times \
            if url and re.match("https://bitcointalk\.org/index\.php\?board=\d+\.\d+$", url)\
            else self.max_retry_times
        if retries <= maxtimes:
            log.msg(format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            log.msg(format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                    level=log.ERROR, spider=spider, request=request, retries=retries, reason=reason)
            self.file.write(url + '\n')