# -*- coding: utf-8 -*-

import json
import codecs
from BitcointalkSpider.items import User, Post, Thread
import time
from BitcointalkSpider.settings import SPIDER_WORK_DIR
import os


class JsonWithEncodingPipeline(object):
#solve outfile code question by output json
	def __init__(self):
		pass
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
				usertime = time.struct_time([0 for i in range(9)])
			userpath = os.path.join(SPIDER_WORK_DIR, "User", str(usertime.tm_year) + str(usertime.tm_mon))
			if os.path.exists(userpath):
				pass
			else:
				os.makedirs(userpath)
			try:
				eachuserfile = os.path.join(userpath, item["name"][0].__str__())
			except:
				eachuserfile = os.path.join(userpath, "NONENAME")
			userfile = codecs.open(eachuserfile, "ab", encoding = "utf-8")
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			userfile.write(line)
			userfile.close()

		if item.__class__ == Thread:
			'''	sort by time
			try:
				time = item["time"][0].__str__()
			else:

			localtime = time.localtime()
			if time.find("at") == -1:
				usertime = time.strptime(time, "%B %d, %Y, %I:%M:%S %p")
			else:
				usertime  = localtime	#aboutly equal, but lastest they date is equal, this is enough
			'''
			Thread_work_dir = os.path.join(SPIDER_WORK_DIR, "Thread")
			if item["ofBoard"] != []:
				Threadpath = reduce(os.path.join, map(lambda x: unicode.encode(x, "utf-8"), item["ofBoard"]), Thread_work_dir)
			else:
				Threadpath = os.path.join(Thread_work_dir, "NONEBOARD")
			if os.path.exists(Threadpath):
				pass
			else:
				os.makedirs(Threadpath)
			eachThreadfile = os.path.join(Threadpath, item["url"].split("=")[1].__str__())
			Threadfile = codecs.open(eachThreadfile, "ab", encoding = "utf-8")
			#There we can add some \n to make it comfortable for people to read
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			Threadfile.write(line)
			Threadfile.close()

		return item

	def spider_closed(self, spider):
		pass

