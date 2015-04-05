# -*- coding: utf-8 -*-

import scrapy


class User(scrapy.Item):
	# store user's infromation
	name = scrapy.Field()
	posts = scrapy.Field()
	activity = scrapy.Field()
	position = scrapy.Field()
	registerDate = scrapy.Field()
	lastDate = scrapy.Field()
	Email = scrapy.Field()
	gender = scrapy.Field()
	age = scrapy.Field()
	bitcoinAddress = scrapy.Field()
	year = scrapy.Field()
	month = scrapy.Field()
	day = scrapy.Field()
    
class Thread(scrapy.Item):
	# store posts' information
	topic = scrapy.Field()
	time = scrapy.Field()
	# include every post'(include re) all content(topic, author, time, content)
	content = scrapy.Field()
	url = scrapy.Field()
	ofBoard = scrapy.Field()
	user = scrapy.Field()
	year = scrapy.Field()
	month = scrapy.Field()
	day = scrapy.Field()
	flag = scrapy.Field()  #Thread if 1 else 0
