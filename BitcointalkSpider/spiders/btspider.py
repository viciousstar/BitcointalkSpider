from datetime import datetime
import ConfigParser
import re
import scrapy
from scrapy.spider import Spider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log
from scrapy.http import Request
from ..items import User, Post, Thread
from BitcointalkSpider.util import incAttr

class btthreadspider(scrapy.spider.Spider):

    name = "btthreadspider"
    allowed_domains = ["bitcointalk.org"]
    start_urls = ["https://bitcointalk.org/index.php"]

    def __init__(self):
        self.maxboardurl = {}
        self.stats = {}
    
    def extractUser(self, response):
        incAttr(self.stats, 'recieveUserNum')
        user = User()
        userinfo = response.xpath("//table[@border = '0'  and @cellpadding = '2']/tr")
        # extract every info form list of  userinfo
        for character in userinfo:
            text = filter(unicode.strip, character.xpath(".//text()").extract())
            if  text != []:
                lenText = len(text)
                textname = text.pop(0)
                if  textname.find("Name") != -1:
                    if len > 1:
                        user["name"] = text
                    else:
                        user["name"] = None
                    continue
                elif  textname.find("Posts") != -1:
                    if len > 1:
                        user["posts"] = text
                    else:
                        user["posts"] = None
                    continue
                elif  textname.find("Activity") != -1:
                    if len > 1:
                        user["activity"] = text
                    else:
                        user["activity"] = None
                    continue
                elif  textname.find("Position") != -1:
                    if len > 1:
                        user["position"] = text
                    else:
                        user["position"] = None
                    continue
                elif  textname.find("Date Registered") != -1:
                    if len > 1:
                        user["registerDate"] = text
                    else:
                        user["registerDate"] = None
                    continue
                elif  textname.find("Last Active") != -1:
                    if len > 1:
                        user["lastDate"] = text
                    else:
                        user["lastDate"] = None
                    continue
                elif  textname.find("Email: ") != -1:
                    if len > 1:
                        user["Email"] = text
                    else:
                        user["Email"] = None
                    continue
                elif  textname.find("Gender") != -1:
                    if len > 1:
                        user["gender"] = text
                    else:
                        user["gender"] = None
                    continue
                elif  textname.find("Age") != -1:
                    if len > 1:
                        user["age"] = text
                    else:
                        user["age"] = None
                    continue
                elif  textname.find("Signature") != -1:
                    if len > 1:
                        user["bitcoinAddress"] = text
                    else:
                        user["bitcoinAddress"] = None
                    continue
                else:
                    incAttr(self.stats, 'ignoreUserAttrNum')
                    log.msg('%s do not extract info in %s!' % response.body, response.url, level = log.ERROR)
            else:
                incAttr(self.stats, 'ignoreUserNum')
                log.msg('%s do not extract info in %s!' % response.body, response.url, level = log.ERROR)
        if user.fields.values() == [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}]:
            incAttr(self.stats, 'ignoreUserNum')
            log.msg('%s do not extract info in %s!' % response.body, response.url, level = log.ERROR)
            return         
        return user

    def extractPost(self, response):
        post = Thread()
        post["topic"] = response.xpath("//*[@id = 'top_subject']/text()")[0].extract().split(":")[1]
        post["content"] = []
        tr =  str(response.xpath("//*[@id = 'quickModForm']/table[1]/tr[1]/@class").extract()[0])
        #every post
        smallPost = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[@class and @class = '%s']" % tr)
        # if we want tocontinue use xpath on exsit xpath, we must add "." to represent the present node
        post["user"] = smallPost[0].xpath("(.//a[@href])[1]/text()").extract()
        post["time"] = smallPost[0].xpath("(.//div[@class = 'smalltext'])[2]//text()").extract()
        post["url"] = response.url
        boardlist = response.xpath("//a[@class = 'nav']/text()").extract()
        #lenBoardlist //a[@class = 'nav']/text() occur two postion (head and tail)
        lenBoardlist = len(boardlist) / 2
        post["ofBoard"] = [boardlist[x] for x in range(0, lenBoardlist)]
        #store every post partly by loop
        for  everyPost in smallPost:            
            smallpost = Post()
            smallpost["user"] = everyPost.xpath("(.//a[@href])[1]/text()").extract()
            smallpost["topic"] = everyPost.xpath(".//*[@class = 'subject']/a/text()").extract()
            smallpost["time"] =  everyPost.xpath("(.//div[@class = 'smalltext'])[2]//text()").extract()
            smallpost["content"] = everyPost.xpath(".//div[@class = 'post']/text()").extract()
            post["content"].append(dict(smallpost))
        yield post

        dup = response.meta['set']
        urls = response.xpath('//a/@href').extract()
        thpattren = re.compile(response.url.rsplit('.', 1)[0] + "\.\d+$")
        userpattren = re.compile("https://bitcointalk\.org/index\.php\?action=profile;u=\d+$")
        for url in urls:
            if thpattren.match(url) and url not in dup:
                dup.add(url)
                rqst = Request(url=url, callback = self.extractPost)
                rqst.meta['set'] = dup
                yield rqst
            elif userpattren.match(url):
                yield Request(url=url, callback = self.extractUser)

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
        if time == None:
            return True #rather crawl more than ignore
        return time >= self.crawler.stats.get_value('last_start_time')

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
        url = response.url
        if self.isNewTime(time):
            urls = response.xpath('//a/@href').extract()
            for url in urls:
                pattren = re.compile("https://bitcointalk\.org/index\.php\?topic=\d+\.0$")
                if pattren.match(url):
                    rqst = Request(url=url, callback = self.extractPost)
                    rqst.meta['set'] = set()
                    rqst.meta['set'].add(url)
                    yield rqst
            k, n = url.rsplit('.', 1)
            n = int(n)
            if k not in self.maxboardurl:
                self.genmax(response)
            mn = self.maxboardurl[k]
            url = ''.join([k, '.', str(n + 40)])
            #generate next board url   
            if n < mn:        
                yield Request(url=url, callback = self.filterPost)  

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

# class btuserspider(scrapy.contrib.spiders.CrawlSpider):
#   name = "btuserspider"
#   allowed_domains = ["bitcointalk.org"]
#   start_urls = ["https://bitcointalk.org/index.php?action=mlist;sort=registered;start=0;desc"]
    
#   rules =  (
#       #rule for use
#       Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?action=profile;u=\d+$", ), ),
#           callback = "extractUser"),
#       Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?action=mlist;sort=registered;start=\d+;desc")))
        
#       )           #may add renz

#   def parse_start_url(self, response):
#       open('login.html', 'w').write(response.body)
#       rsq = scrapy.Request.from_response(
#           response,
#           formdata={'user': 'vicious_starr%%40163.com', 'passwrd': 'qwer1234'},
#           callback=self.after_login
#       )
#       print rsq.headers
#       print  '\n\n\n\n\n\n'
#       return rsq
    
#   def after_login(self, response):
#       open('after_login.html', 'w').write(response.body)
#       rsq = scrapy.Request(url = 'https://bitcointalk.org/index.php?action=login2%3bsa=check%3bmember=379410', headers = {'Host': 'bitcointalk.org',
#                 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0',
#                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                 'Accept-Language': 'en-US,en;q=0.5',
#                 'Accept-Encoding': 'gzip, deflate',
#                 #'Cookie':  'SMFCookie129=a%3A4%3A%7Bi%3A0%3Bs%3A6%3A%22379410%22%3Bi%3A1%3Bs%3A40%3A%2269f88edb7ee63f5b54f4dfdd532d4cd7a8b6bd29%22%3Bi%3A2%3Bi%3A1426168224%3Bi%3A3%3Bi%3A0%3B%7D',
#                 'Connection': 'keep-alive',
#                 'If-Modified-Since': 'Thu, 12 Mar 2015 08:52:12 GMT',
#                 'Cache-Control': 'max-age=0'})
#       print rsq.headers
#       print  '\n\n\n\n\n\n'
#       return rsq
#   def after_login2(self, response):
#       open('after_login2.html', 'w').write(response.body)

#   def extractUser(self, response):
#       user = User()
#       userinfo = response.xpath("//table[@border = '0'  and @cellpadding = '2']/tr")
#       # extract every info form list of  userinfo
#       for character in userinfo:
#           text = filter(unicode.strip, character.xpath(".//text()").extract())
#           if  text != []:
#               lenText = len(text)
#               textname = text[0]
#               text.pop(0)
#               if  textname.find("Name") != -1:
#                   if len > 1:
#                       user["name"] = text
#                   else:
#                       user["name"] = None
#                   continue
#               if  textname.find("Posts") != -1:
#                   if len > 1:
#                       user["posts"] = text
#                   else:
#                       user["posts"] = None
#                   continue
#               if  textname.find("Activity") != -1:
#                   if len > 1:
#                       user["activity"] = text
#                   else:
#                       user["activity"] = None
#                   continue
#               if  textname.find("Position") != -1:
#                   if len > 1:
#                       user["position"] = text
#                   else:
#                       user["position"] = None
#                   continue
#               if  textname.find("Date Registered") != -1:
#                   if len > 1:
#                       user["registerDate"] = text
#                   else:
#                       user["registerDate"] = None
#                   continue
#               if  textname.find("Last Active") != -1:
#                   if len > 1:
#                       user["lastDate"] = text
#                   else:
#                       user["lastDate"] = None
#                   continue
#               if  textname.find("Email: ") != -1:
#                   if len > 1:
#                       user["Email"] = text
#                   else:
#                       user["Email"] = None
#                   continue
#               if  textname.find("Gender") != -1:
#                   if len > 1:
#                       user["gender"] = text
#                   else:
#                       user["gender"] = None
#                   continue
#               if  textname.find("Age") != -1:
#                   if len > 1:
#                       user["age"] = text
#                   else:
#                       user["age"] = None
#                   continue
#               if  textname.find("Signature") != -1:
#                   if len > 1:
#                       user["bitcoinAddress"] = text
#                   else:
#                       user["bitcoinAddress"] = None
#                   continue
#           else:
#               continue
#       return user