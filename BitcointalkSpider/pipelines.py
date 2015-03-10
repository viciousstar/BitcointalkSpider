# -*- coding: utf-8 -*-

import json
import codecs
from BitcointalkSpider.items import User, Post, Thread
from BitcointalkSpider.settings import SPIDER_WORK_DIR
import os
from datetime import datetime
import pymongo
from pymongo import MongoClient

class JsonWithEncodingPipeline(object):
#solve outfile code question by output json
	def __init__(self):
		try:
			self.client = MongoClient()
			self.db = client.bitdb
		except:
			print 'Please start Mongod.'
			raise BaseException()
		self.configfile = open('BitcointalkSpider/config.py', 'r+')
        config = ConfigParser.ConfigParser()
        config.readfp(self.configfile)
        self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
        try:
        	self.db.creat_collection(str(self.time.year) + str(self.time.month))
        except:
        	pass
        self.clt = self.db[str(self.time.year) + str(self.time.month)]

	def process_item(self, item, spider):
		if  item.__class__ == User:
		#time format 
		#time.strptime(str, "%B %d, %Y, %H:%M:%S %p")
			rtimelen = len(item["registerDate"])
			localtime = time.localtime()
			try:
				if rtimelen == 1:
					usertime = time.strptime(item["registerDate"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
				if rtimelen == 2:
					usertime  = localtime
			except:
				usertime = None
			if usertime > self.time
				userpath = os.path.join(SPIDER_WORK_DIR, "User")
				if os.path.exists(userpath):
					pass
				else:
					os.makedirs(userpath)
				self.userfile = codecs.open(str(self.time.year) + str(self.time.month), "ab", encoding = "utf-8")
				line = json.dumps(dict(item), ensure_ascii=False) + "\n"
				self.userfile.write(line)
			    lastDate = datetime.strptime(item['lastDate'][0], '%B %d, %Y, %I:%M:%S %p')
        		registerDate = datetime.strptime(item['registerDate'][0], '%B %d, %Y, %I:%M:%S %p')
        		item['registerDate'] = registerDate
        		item['year'] = registerDate.year
        		item['month'] = registerDate.month
        		item['day'] = registerDate.day 
			    item['activity'] = int(item['activity'][0]) 
        		item['posts'] = int(item['posts'][0])
        		self.clt.save(item)
			else:
				return None
		if item.__class__ == Thread:
			try:
				time = item["time"][0].__str__()
				if time.find("at") == -1:
					usertime = time.strptime(time, "%B %d, %Y, %I:%M:%S %p")
				else:
					usertime  = localtime	#aboutly equal, but lastest they date is equal, this is enough
			except:
				time = None
			if time > self.time:
				Thread_work_dir = os.path.join(SPIDER_WORK_DIR, "Thread")
				self.Threadfile = codecs.open(Thread_work_dir + str(self.time.year) + str(self.time.month), "ab", encoding = "utf-8")
				#There we can add some \n to make it comfortable for people to read
				line = json.dumps(dict(item), ensure_ascii=False) + "\n"
				self.Threadfile.write(line)
				time = datetime.datetime.strptime(item['time'][0], '%B %d, %Y, %I:%M:%S %p')
        		item['time'] = time
        		item['year'] = time.year
        		item['month'] = time.month
        		item['day'] = time.day 
			    item['activity'] = int(item['activity'][0]) 
        		item['posts'] = int(item['posts'][0])
        		self.clt.save(item)
			else:
				return None
	def spider_closed(self, spider):
		self.userfile.close()
		self.Threadfile.close()
		self.configfile.close()
		self.client.close()

