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

class JsonWithEncodingPipeline(object):
#solve outfile code question by output json
    def open_spider(self, spider):
        self.nowtime = datetime.today()
        try:
            self.client = MongoClient()
            self.db = self.client.bitdb
        except:
            log.msg(self.nowtime.isoformat() + 'Start Mongod Fail')
            raise Exception('Start Mongod Fail')
        self.time = spider.crawler.stats.get_value('last_start_time')
        thcltname = ''.join(['thread', str(self.time.year), str(self.time.month)])
        usercltname = ''.join(['user', str(self.time.year), str(self.time.month)])

        try:
            self.thclt = self.db.create_collection('thread' + str(self.time.year) + str(self.time.month))
            self.userclt = self.db.create_collection('user' + str(self.time.year) + str(self.time.month))
        except pymongo.errors.CollectionInvalid:
            self.thclt = self.db[thcltname]
            self.userclt = self.db[usercltname]
    

    def process_item(self, item, spider):
        localtime = datetime.today()
        if  item.__class__ == User:
            #distinguish 'Today at xxxxxx' time format
            try:
                usertime = timeFormat(item['registerDate'][-1])
            except:
                usertime = None
            if usertime and usertime > self.time:
                userpath = os.path.join(SPIDER_DATA_DIR, "User")
                if os.path.exists(userpath):
                    pass
                else:
                    os.makedirs(userpath)
                self.userfile = codecs.open(os.path.join(userpath,str(self.time.year) + str(self.time.month)), "ab", encoding = "utf-8")
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.userfile.write(line)
                ltimelen = len(item["lastDate"])
                item['registerDate'] = usertime
                item['year'] = registerDate.year
                item['month'] = registerDate.month
                item['day'] = registerDate.day 
                item['activity'] = int(item['activity'][0]) 
                item['posts'] = int(item['posts'][0])
                self.userclt.save(dict(item))
        
        if item.__class__ == Thread:
            try:
                threadtime = timeFormat(item['time'][-1])
            except:
                threadtime = None
            if threadtime and threadtime > self.time:
                threadpath = os.path.join(SPIDER_DATA_DIR, "Thread")
                if os.path.exists(threadpath):
                    pass
                else:
                    os.makedirs(threadpath)
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
    
    def close_spider(self, spider):
        print self.thclt
        print self.userclt
        print '\n\n\n\n'
        plotThread(self.thclt, self.time).plot()
        plotUser(self.userclt, self.time).plot()
        self.userfile.close()
        self.threadfile.close()
        self.client.close()
