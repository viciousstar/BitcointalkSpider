from scrapy import signals
from datetime import datetime
import ConfigParser
from BitcointalkSpider.config import  jobdir
from scrapy.dupefilter import RFPDupeFilter
import re

class FilterurlExtension(object):
    """Filter url that later than the last spider starting, and update config.py"""
    def __init__(self):
        pass

    @classmethod
    def form_crawler(cls, crawler):
        ext = cls()

        crawler.signals.connect(ext.spider_opened, signal = signals.spider_opened)
        # crawler.signals.connect(ext.spider_response, signal = signals.response_downloaded)
        crawler.signals.connect(ext.spider_closed, signal = signals.spider_closed)

        return ext

    def spider_opened(self, spider):
        self.configfile = open('BitcointalkSpider/config.py', 'r+')
        self.config = ConfigParser.ConfigParser()
        config.readfp(self.configfile)
        self.time = datetime.strptime(config.get('SPIDER', 'start_time'), '%Y-%m-%dT%H:%M:%S.%f')
        self.config.set('SPIDER', 'start_time', datetime.isoformat())

        print "\nstart time read finish."

    
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
            self.config.set('SPIDER', 'finish_time', datetime.isoformat())
            self.config.write(self.configfile)
            self.configfile.close()
            # requestfile = open(jobdir + '/ownrequest.seen')
            # spider.
        except:
            print 'Write config fail!'

class SaveRequsetSeen(RFPDupeFilter):

    def request_seen(self, request):
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        
        if not re.match('board=\d+' ,request.url):       
            if self.file:
                self.file.write(fp + os.linesep)
        else:
            pass