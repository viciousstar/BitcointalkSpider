# -*- coding: utf-8 -*-

import json
import codecs
import os
from datetime import datetime
import pymongo
from scrapy import log
from pymongo import MongoClient
import ConfigParser
from .items import User, Post, Thread
from .settings import SPIDER_DATA_DIR, SPIDER_PRO_DIR
from .Mongodb.plotAllThread import plotThread
from .Mongodb.plotAllUser import plotUser
from BitcointalkSpider.util import timeFormat
from BitcointalkSpider.util import creatPath
from BitcointalkSpider.util import incAttr

class JsonWithEncodingPipeline(object):
#solve out file code problem by output json
    def open_spider(self, spider):
        self.nowtime = datetime.today()
        try:
            self.client = MongoClient()
            self.db = self.client.bitdb
        except:
            log.msg('Start Mongod Fail', level=log.ERROR)
            raise Exception('Start Mongod Fail')
        self.stats = spider.crawler.stats
        self.stats.set_value('saveUserNum', 0)
        self.stats.set_value('saveThreadNum', 0)
        self.time = self.stats.get_value('last_start_time')
        #everymonth has its collection 
        thcltname = ''.join(['thread', str(self.time.year), str(self.time.month)])
        usercltname = ''.join(['user', str(self.time.year), str(self.time.month)])
        #if it not has collection it will creat itself
        self.thclt = self.db[thcltname]
        self.userclt = self.db[usercltname]
        userpath = os.path.join(SPIDER_DATA_DIR, "User")
        threadpath = os.path.join(SPIDER_DATA_DIR, "Thread")
        creatPath(userpath, threadpath)
        self.userfile = None
        self.threadfile = None
  
    def process_item(self, item, spider):
        localtime = datetime.today()

        if  item.__class__ == User:
            if item['registerDate']:
                usertime = timeFormat(item['registerDate'][-1].strip())
            else:
                usertime = None
            
            if item['lastDate']:
                lastDate = timeFormat(item['lastDate'][-1].strip())
            else:
                lastDate = None
            
            if usertime and usertime > self.time:
                if not self.userfile:
                    self.userfile = codecs.open(os.path.join(userpath,str(self.time.year) + str(self.time.month)), "ab", encoding = "utf-8")
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.userfile.write(line)
                item['lastDate'] = lastDate
                item['registerDate'] = usertime
                item['year'] = registerDate.year
                item['month'] = registerDate.month
                item['day'] = registerDate.day 
                item['activity'] = int(item['activity'][0]) 
                item['posts'] = int(item['posts'][0])
                self.userclt.save(dict(item))
                self.stats.inc_value('saveUserNum')
        if item.__class__ == Thread:
            # print item
            if item['time']:
                threadtime = timeFormat(item['time'][-1].strip())
            else:
                threadtime = None
            if threadtime and threadtime > self.time:
                if not self.threadfile:
                    self.threadfile = codecs.open(os.path.join(threadpath, str(self.time.year) + str(self.time.month)), "ab", encoding = "utf-8")
                #There we can add some \n to make it comfortable for people to read
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.threadfile.write(line)
                time = threadtime
                item['time'] = time
                item['year'] = time.year
                item['month'] = time.month
                item['day'] = time.day 
                self.thclt.save(dict(item))
                self.stats.inc_value('saveThreadNum')

    def close_spider(self, spider):
        plotThread(self.thclt, self.time).plot()
        plotUser(self.userclt, self.time).plot()
        # try:
        self.userfile.close()
        self.threadfile.close()
        self.client.close()
        # except:
        # log.msg('pipeline file close fail')