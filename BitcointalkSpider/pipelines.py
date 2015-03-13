# -*- coding: utf-8 -*-

import json
import codecs
from BitcointalkSpider.items import User, Post, Thread
from BitcointalkSpider.settings import SPIDER_WORK_DIR
import os
from datetime import datetime
import pymongo
from pymongo import MongoClient
import ConfigParser

class JsonWithEncodingPipeline(object):
#solve outfile code question by output json
	def __init__(self):
		try:
			self.file = open('stat.info', 'a+')
			self.count = 0
			self.client = MongoClient()
			self.db = self.client.bitdb
			print self.db
		except:
			print 'Please start Mongod.'
			return
		self.configfile = open('BitcointalkSpider/config.cfg', 'r+')
		config = ConfigParser.ConfigParser()
		config.readfp(self.configfile)
		time = config.get('SPIDER', 'start_time')
		self.time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
		try:
			self.db.create_collection(str(self.time.year) + str(self.time.month))
		except:
			print 'fail to creat collection'
		self.clt = self.db[str(self.time.year) + str(self.time.month)]

	def process_item(self, item, spider):
		localtime = datetime.today()
		if  item.__class__ == User:
		#time format 
		#time.strptime(str, "%B %d, %Y, %H:%M:%S %p")
			rtimelen = len(item["registerDate"])
			try:
				if rtimelen == 1:
					usertime = datetime.strptime(item["registerDate"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
				if rtimelen == 2:
					usertime  = localtime
			except:
				usertime = None
			if usertime and usertime > self.time:
				userpath = os.path.join(SPIDER_WORK_DIR, "User")
				if os.path.exists(userpath):
					pass
				else:
					os.makedirs(userpath)
				self.userfile = codecs.open(str(self.time.year) + str(self.time.month), "ab", encoding = "utf-8")
				line = json.dumps(dict(item), ensure_ascii=False) + "\n"
				self.userfile.write(line)
				try:
					lastDate = datetime.strptime(item['lastDate'][0], '%B %d, %Y, %I:%M:%S %p')
				except:
					lastDate = datetime.today()
				registerDate = datetime.strptime(item['registerDate'][0], '%B %d, %Y, %I:%M:%S %p')
				item['registerDate'] = registerDate
				item['year'] = registerDate.year
				item['month'] = registerDate.month
				item['day'] = registerDate.day 
				item['activity'] = int(item['activity'][0]) 
				item['posts'] = int(item['posts'][0])
				self.clt.save(item)
				self.count += 1
				print 'save user successfully \n\n\n\n\n\n'
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
				Thread_work_dir = os.path.join(SPIDER_WORK_DIR, "Thread")
				if os.path.exists(Thread_work_dir):
					pass
				else:
					os.makedirs(Thread_work_dir)
				self.Threadfile = codecs.open(Thread_work_dir + str(self.time.year) + str(self.time.month), "ab", encoding = "utf-8")
				#There we can add some \n to make it comfortable for people to read
				line = json.dumps(dict(item), ensure_ascii=False) + "\n"
				self.Threadfile.write(line)
				time = datetime.strptime(item['time'][0], '%B %d, %Y, %I:%M:%S %p')
				item['time'] = time
				item['year'] = time.year
				item['month'] = time.month
				item['day'] = time.day 
				item['activity'] = int(item['activity'][0]) 
				item['posts'] = int(item['posts'][0])
				self.clt.save(item)
				print 'save thread successfully \n\n\n\n\n\n'
				self.count += 1
			else:
				return None
	def spider_closed(self, spider):
		self.file.write(self.count)
		self.userfile.close()
		self.Threadfile.close()
		self.configfile.close()
		self.client.close()
		self.file.close()
