from datetime import datetime
import ConfigParser
import re
import urllib2
import scrapy
from scrapy.spider import Spider
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy import log
from scrapy.http import Request
from ..items import User, Thread
from BitcointalkSpider.util import incAttr



class btuserspider(scrapy.spider.Spider):
    name = "btuserspider"
    allowed_domains = ["bitcointalk.org"]

    def start_requests(self):
        return [scrapy.FormRequest(
            "https://bitcointalk.org/index.php?action=login2",
            formdata={'user': 'vicious_star@163.com', 'passwrd': 'qwer1234', 'cookieneverexp': 'on'},
            callback=self.after_login
        )]
        
      
    def after_login(self, response):
        return scrapy.FormRequest(
            "https://bitcointalk.org/index.php?action=mlist;sort=registered;start=0;desc",
            callback=self.extractUserUrl
        )

    def extractUserUrl(self,response):
        pattern = re.compile(r'\d+')
        time = response.xpath('//*[@id="bodyarea"]/table[2]/tr[3]/td[10]/text()').extract()[0].split('-')
        time = datetime(int(time[0]), int(time[1]), int(time[2]), 23, 59, 59)
        urls = response.xpath('//*[@id="bodyarea"]/table[2]/tr/td[2]/a/@href').extract()[1:]
        
        if self.isNewTime(time):
            for url in urls:
                yield Request(url = url, callback = self.extractUser)
            cur = int(pattern.findall(response.xpath('//*[@id="bodyarea"]/div/div/b[3]/a/text()').extract()[0])[1])
            last = int(pattern.findall(response.xpath('//*[@id="bodyarea"]/div/div/text()[3]').extract()[0])[0])
            if cur < last:
                nexturl = "https://bitcointalk.org/index.php?action=mlist;sort=registered;start=%d;desc" % (int(pattern.findall(response.url)[0]) + 30)
                yield Request(url = nexturl, callback = self.extractUserUrl)

    def extractUser(self, response):
        user = User()
        userinfo = response.xpath("//table[@border = '0'  and @cellpadding = '2']/tr")
        # extract every info form list of  userinfo
        for character in userinfo:
            text = filter(unicode.strip, character.xpath(".//text()").extract())
            if  text != []:
                lenText = len(text)
                textname = text[0]
                text.pop(0)
                if  textname.find("Name") != -1:
                    if len > 1:
                        user["name"] = text
                    else:
                        user["name"] = None
                    continue
                if  textname.find("Posts") != -1:
                    if len > 1:
                        user["posts"] = text
                    else:
                        user["posts"] = None
                    continue
                if  textname.find("Activity") != -1:
                    if len > 1:
                        user["activity"] = text
                    else:
                        user["activity"] = None
                    continue
                if  textname.find("Position") != -1:
                    if len > 1:
                        user["position"] = text
                    else:
                        user["position"] = None
                    continue
                if  textname.find("Date Registered") != -1:
                    if len > 1:
                        user["registerDate"] = text
                    else:
                        user["registerDate"] = None
                    continue
                if  textname.find("Last Active") != -1:
                    if len > 1:
                        user["lastDate"] = text
                    else:
                        user["lastDate"] = None
                    continue
                if  textname.find("Email: ") != -1:
                  if len > 1:
                      user["Email"] = text
                  else:
                      user["Email"] = None
                  continue
                if  textname.find("Gender") != -1:
                    if len > 1:
                        user["gender"] = text
                    else:
                        user["gender"] = None
                    continue
                if  textname.find("Age") != -1:
                    if len > 1:
                        user["age"] = text
                    else:
                        user["age"] = None
                    continue
                if  textname.find("Signature") != -1:
                    if len > 1:
                        user["bitcoinAddress"] = text
                    else:
                        user["bitcoinAddress"] = None
                    continue
            else:
                continue
        return user

    def isNewTime(self, time):
        #rather crawl more than ignore
        return time is None or time >= self.crawler.stats.get_value('last_start_time')
