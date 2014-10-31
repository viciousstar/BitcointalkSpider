# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

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
		if  item.__class__ == User
		#time format 
		#time.strptime(str, "%B %d, %Y, %H:%M:%S %p")
			rtimelen = len(item["registerDate"])
			localtime = time.localtime()
			if rtimelen == 1:
				usertime = time.strptime(item["registerDate"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
			if rtimelen == 2:
				usertime  = localtime
			userpath = os.path.join(SPIDER_WORK_DIR, usertime.tm_year + usertime.tm_mon)
			if os.path.exsits(userpath):
				pass
			else:
				os.path.makedirs(userpath)
			userfile = codecs.open(userpath + item["name"][0].__str__(), "ab", encoding = "utf-8")
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			userfile.write(line)
			userfile.close()

		if item.__class__ == Thread:
			rtimelen = len(item["registerDate"])
			localtime = time.localtime()
			if rtimelen == 1:
				usertime = time.strptime(item["time"][0].__str__(), "%B %d, %Y, %I:%M:%S %p")
			if rtimelen == 2:
				usertime  = localtime	#aboutly equal, but lastest they date is equal, this is enough
			Threadpath = reduce(os.path.join, map(lambda x: unicode.encode(x, "utf-8"), item["ofBoard"], SPIDER_WORK_DIR)
			if os.path.exsits(Threadpath):
				pass
			else:
				os.path.makedirs(Threadpath)
			Threadfile = codecs.open(Threadpath + item["url"].spilt("=")[1].__str__(), "ab", encoding = "utf-8")
			#There we can add some \n to make it comfortable for people to read
			line = json.dumps(dict(item), ensure_ascii=False) + "\n"
			userfile.write(line)
			Threadfile.close()

		return item

	def spider_closed(self, spider):
		pass


'''
some standard datas

{"name": ["Uri"], 
"gender": [], 
"age": ["N/A"], 
"posts": ["1"], 
"lastData": ["August 10, 2014, 03:50:08 PM"], 
"activity": ["1"], 
"bitcoinAddress": [], 
"position": ["Newbie"], 
"Email": ["hidden"]},
{"content": [{"topic": ["\u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df"], 
"content": ["\u05e9\u05dc\u05d5\u05dd \u05dc\u05db\u05d5\u05dc\u05dd,", "\u05de\u05d9\u05e9\u05d4\u05d5 \u05de\u05db\u05d9\u05e8 \u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05d8\u05d5\u05d1\u05d9\u05dd \u05d1\u05e8\u05e9\u05ea \u05e9\u05d0\u05e4\u05e9\u05e8 \u05dc\u05d4\u05e8\u05d5\u05d5\u05d9\u05d7 \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df?"], 
"user": ["johnatan32"], 
"time": ["May 11, 2014, 04:32:14 PM"]}, {"topic": ["Re: \u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df"], 
"content": ["\u05d4\u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05d4\u05dd \u05e2\u05e4\"\u05e8 (\u05db\u05de\u05d5) \u05d4\u05d9\u05de\u05d5\u05e8\u05d9\u05dd - \u05dc\u05d0 \u05de\u05db\u05d9\u05e8 \u05d0\u05e3 \u05d0\u05d7\u05d3 \u05de\u05d4\u05dd... "], 
"user": ["r1973"], 
"time": ["May 11, 2014, 07:40:39 PM"]}], 
"ofBoard": ["Bitcoin Forum", "Local", "\u05e2\u05d1\u05e8\u05d9\u05ea (Hebrew)", "\u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df"], 
"url": "https://bitcointalk.org/index.php?topic=604954.0", "topic": " \u05de\u05e9\u05d7\u05e7\u05d9\u05dd \u05e2\u05dc \u05d1\u05d9\u05d8\u05e7\u05d5\u05d9\u05df \u00a0(Read 323 times)\n\t\t\t\t", "user": ["johnatan32"], 
"time": ["May 11, 2014, 04:32:14 PM"]},

'''
