from datetime import datetime
import ConfigParser
import re
import os
import json
from scrapy.dupefilter import RFPDupeFilter
from scrapy import signals
from scrapy import log
from .settings import SPIDER_PRO_DIR
class FilterurlExtension(object):
    """Filter url that later than the last spider starting, and update config.cfg"""
    def __init__(self, stats):
        self.time = datetime.today()
        self.stats = stats
        self.spider_opened()
    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.stats)
        # ext.engine = crawler.engine 
        # crawler.signals.connect(ext.spider_opened, signal = signals.engine_started)
        crawler.signals.connect(ext.spider_closed, signal = signals.spider_closed)
        # crawler.signals.connect(ext.spider_received, signal = signals.response_received)
        return ext

    def spider_opened(self):
        try:
            self.configfile = open(os.path.join(SPIDER_PRO_DIR, 'config.cfg'), 'r+')
            self.config = ConfigParser.ConfigParser()
            self.config.readfp(self.configfile)
            self.time = datetime.strptime(self.config.get('SPIDER', 'start_time'), '%Y-%m-%dT%H:%M:%S.%f')
        except:
            self.time = datetime.today()
        self.stats.set_value('last_start_time', self.time)
        self.config.set('SPIDER', 'start_time', datetime.today().isoformat())
        log.msg(self.time.isoformat() + "Read config finish.") 
    
    # def spider_response(self, response, request, spider):
    #     if spider.name == 'btthreadspider':
    #         time = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[@class and @class = '%s']" % tr)[0].xpath("(.//div[@class = 'smalltext'])[2]/text()").extract()[0]
    #     else:
    #         time = spider.extractUser(response)['registerDate'][0]
    #     try:
    #         time = datetime.strptime(time, '%B %d, %Y, %I:%M:%S %p')
    #     except:
    #         time = datetime.today()
    #     if time > self.time:
    #         pass
    #     else:
    #         response = None
    #     request = None
    def spider_closed(self, spider):
        try:
            self.config.set('SPIDER', 'finish_time', datetime.today().isoformat())
            self.config.write(open(os.path.join(SPIDER_PRO_DIR, 'config.cfg'), 'w'))
            self.configfile.close()
            log.msg(self.time.isoformat() + 'Write config finish')
            info = dict(self.stats.get_stats())
            info.update(self.stats.spider_stats)
            statinfo = json.dumps(info)
            f = open(os.path.join(SPIDER_PRO_DIR, 'stat.info'), 'a+').write(statinfo)
            f.close()
        except:
            log.msg(self.time.isoformat() + 'Write config fail!')

class SaveRequestSeen(RFPDupeFilter):
    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)       
        if not re.match('board=\d+$|topic=\d+\.0$' ,request.url):       
            if self.file:
                self.file.write(fp + os.linesep)
        else:
            pass