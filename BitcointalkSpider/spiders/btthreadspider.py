from datetime import datetime
import ConfigParser
import re
import scrapy
from scrapy.spider import Spider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log
from scrapy.http import Request
from ..items import User, Thread
from BitcointalkSpider.util import incAttr

class btthreadspider(scrapy.spider.Spider):

    name = "btthreadspider"
    allowed_domains = ["bitcointalk.org"]
    start_urls = ["https://bitcointalk.org/index.php"]

    def __init__(self):
        self.maxboardurl = {}   
        self.stats = {}
    
    def extractPost(self, response):
        posts = response.xpath('//div[@style="margin: 0 5ex;"]')
        infos = response.xpath('//b/text()')
        ofBoard = response.xpath('//h2/text()').extract()[0].split(' => ')[:-1]
        n = len(posts)

        for i in range(n):
            thread = Thread()
            thread['url'] = response.url
            thread['topic'] = infos[i*3].extract()
            thread['user'] = infos[i*3+1].extract()
            thread['time'] = infos[i*3+2].extract()
            thread['content'] = posts[i].xpath('.//text()').extract()
            thread['flag'] = 0 if i==0 else 1
            thread['ofBoard'] = ofBoard
            yield thread

    def parse(self, response):
        #just crawl the first url
        for mainboard in response.xpath('//*[@id="bodyarea"]/div'):
            for board in mainboard.xpath('./table/tr'):
                url = board.xpath('(./td)[2]//a/@href').extract()
                if url:
                    url = url[0]
                else:
                    continue
                time = filter(lambda x : len(x.strip()), board.xpath('(./td)[4]//text()').extract())
                if time == []:
                    incAttr(self.stats, 'ignoreBoardNum')
                    log.msg('The board %s do not have time.' %url, level=log.ERROR)
                    continue
                time = self.timeFormat(time[-1].strip())
                if self.isNewTime(time):
                    yield Request(url=url, callback = self.filterPost)
            
    def isNewTime(self, time):
        #rather crawl more than ignore
        return time is None or time >= self.crawler.stats.get_value('last_start_time')

    def filterPost(self, response):
        if response.xpath("//*[@id='bodyarea']/div[2][@style='margin-bottom: 3ex; ']"): #if has child board
            for board in response.xpath('//*[@id="bodyarea"]/div[2]/table/tr')[1 :]:      #the list[0] is empty
                url = board.xpath('(./td)[2]//a/@href').extract()
                if url:
                    url = url[0]
                else:
                    continue
                if url:     #some board have some subboard 
                    time = filter(lambda x : len(x.strip()), board.xpath('(./td)[4]//text()').extract())
                    if not time:
                        incAttr(self.stats, 'ignoreSubboardNum')
                        log.msg('The board %s do not have time.' %url, level=log.ERROR)
                        continue
                    time = self.timeFormat(time[-1].strip())
                    if self.isNewTime(time):
                        yield Request(url=url, callback = self.filterPost)
            timelist = response.xpath('//*[@id="bodyarea"]/div[3]/table/tr[2]/td[7]/span//text()').extract()
        else:
            timelist = response.xpath('//*[@id="bodyarea"]/div[2]/table/tr[2]/td[7]/span//text()').extract()

        if len(timelist) == 6:
            time = self.timeFormat(timelist[2].strip())
        else:
            time = self.timeFormat(timelist[0].strip())
        if self.isNewTime(time):
            urls = response.xpath('//a/@href').extract()
            for url in urls:
                pattren = re.compile("https://bitcointalk\.org/index\.php\?topic=\d+\.0$")
                if pattren.match(url):
                    printurl = '?action=printpage;'.join(url.rsplit('?', 1))
                    yield Request(url=printurl, callback = self.extractPost)
            #gen next board url 
            nexturl = response.url
            k, n = nexturl.rsplit('.', 1)
            n = int(n)
            if k not in self.maxboardurl:
                self.genmax(response)
            mn = self.maxboardurl[k]
            nexturl = ''.join([k, '.', str(n + 40)])
            #generate next board url   
            if n < mn:        
                yield Request(url=nexturl, callback = self.filterPost)  

    def timeFormat(self, time):
        try:
            if 'at' in time:
                today = datetime.today()
                time = datetime.strptime(time.strip(), 'at %I:%M:%S %p')
                time = time.replace(today.year, today.month, today.day)
            else:
                if 'on' in time:
                    time = datetime.strptime(time.strip(), "on %B %d, %Y, %I:%M:%S %p")
                else:
                    time = datetime.strptime(time.strip(), "%B %d, %Y, %I:%M:%S %p")

            return time
        except:
            log.msg('timeFormat fail.', level = log.ERROR)
            return None

    def genmax(self, response):
        #generate the max url in the board url
        #else deal with some board pages just having one page
        boards = response.xpath('//*[@id="toppages"]/a/@href').extract()
        lasturl = boards[-1] if boards else response.url
        key, value = lasturl.rsplit('.', 1)
        value = int(value)
        self.maxboardurl.update({key: value})



#user authentication
