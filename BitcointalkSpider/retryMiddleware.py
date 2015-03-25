import re
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
from scrapy import log
from scrapy import signals
class MyRetryMiddleware(RetryMiddleware):
    """docstring for MyRetryMiddleware"""
    def __init__(self, settings):
        super(MyRetryMiddleware, self).__init__(settings)
        self.max_retry_main_times = settings.getint('RETRY_MAIN_TIMES')
        self.path = settings.get('SPIDER_RETRYURL_DIR')
    @classmethod
    def from_crawler(cls, crawler):
        rt = cls(crawler.settings)
        crawler.signals.connect(rt.spider_opened, signal = signals.spider_opened)
        crawler.signals.connect(rt.spider_closed, signal = signals.spider_closed)
        return rt
    def spider_opened(self):
        try:
            self.file = open(self.path, 'a+')
        except:
            log.msg("Can not open retryUrl file in %s" %self.path, level = log.ERROR)
            self.file = None
    def spider_closed(self):       
        self.file.close() if self.file else None

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