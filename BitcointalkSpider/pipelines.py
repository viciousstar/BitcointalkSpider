# -*- coding: utf-8 -*-

import json
import codecs
from .items import User, Post, Thread
from .settings import SPIDER_DATA_DIR, SPIDER_PRO_DIR
from .Mongodb.plotAllThread import plotThread
from .Mongodb.plotAllUser import plotUser
import os
from datetime import datetime
import pymongo
from scrapy import log
from pymongo import MongoClient
import ConfigParser

class JsonWithEncodingPipeline(object):
#solve outfile code question by output json
	def __init__(self):
		self.nowtime = datetime.today()
		try:
			self.client = MongoClient()
			self.db = self.client.bitdb
		except:
			log.msg(self.nowtime.isoformat() + 'Start Mongod Fail')
			raise Exception('Start Mongod Fail')
		self.configfile = open(os.path.join(SPIDER_PRO_DIR, 'config.cfg'), 'r')
		config = ConfigParser.ConfigParser() 
		config.readfp(self.configfile)
		time = config.get('SPIDER', 'start_time')
		self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
		try:
			self.thclt = self.db.create_collection('thread' + str(self.time.year) + str(self.time.month))
			self.userclt = self.db.create_collection('user' + str(self.time.year) + str(self.time.month))
		except:
			log.msg(self.nowtime.isoformat() + 'Fail to creat collection')
	def process_item(self, item, spider):
		localtime = datetime.today()
		if  item.__class__ == User:
			#distinguish 'Today at xxxxxx' time format
			rtimelen = len(item["registerDate"])
			try:
				if rtimelen == 1:
					usertime = datetime.strptime(item["registerDate"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
				if rtimelen == 2:
					usertime  = localtime
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
				try:
					if ltimelen == 1:
						lastDate = datetime.strptime(item["lastDate"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
					if ltimelen == 2:
						lastDate  = localtime 
				except:
					lastDate = datetime.today()
				registerDate = datetime.strptime(item['registerDate'][0], '%B %d, %Y, %I:%M:%S %p')
				item['registerDate'] = registerDate
				item['year'] = registerDate.year
				item['month'] = registerDate.month
				item['day'] = registerDate.day 
				item['activity'] = int(item['activity'][0]) 
				item['posts'] = int(item['posts'][0])
				self.userclt.save(dict(item))
			else:
				return None
	
		if item.__class__ == Thread:
			try:
				time = item["time"][0].__str__()
				if time.find("Today") == -1:
					usertime = datetime.strptime(time, "%B %d, %Y, %I:%M:%S %p")
				else:
					usertime  = localtime	#aboutly equal, but lastest they date is equal, this is enough
			except:
				usertime = None
			if usertime and usertime > self.time:
				Thread_work_dir = os.path.join(SPIDER_DATA_DIR, "Thread")
				if os.path.exists(Thread_work_dir):
					pass
				else:
					os.makedirs(Thread_work_dir)
				self.Threadfile = codecs.open(os.path.join(Thread_work_dir,str(self.time.year) + str(self.time.month)), "ab", encoding = "utf-8")
				#There we can add some \n to make it comfortable for people to read
				line = json.dumps(dict(item), ensure_ascii=False) + "\n"
				self.Threadfile.write(line)
				time = datetime.strptime(item['time'][0], '%B %d, %Y, %I:%M:%S %p')
				item['time'] = time
				item['year'] = time.year
				item['month'] = time.month
				item['day'] = time.day 
				self.thclt.save(dict(item))
			else:
				return None
	
	def close_spider(self, spider):
		plotThread(self.thclt).plot()
		plotUser(self.userclt).plot()
		self.userfile.close()
		self.Threadfile.close()
		self.configfile.close()
		self.client.close()
