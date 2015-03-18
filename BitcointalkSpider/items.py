# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class  User(scrapy.Item):
	# store user's infromation
	name = scrapy.Field()
	posts = scrapy.Field()
	activity = scrapy.Field()
	position = scrapy.Field()
	registerDate= scrapy.Field()
	lastDate = scrapy.Field()
	Email = scrapy.Field()
	gender = scrapy.Field()
	age = scrapy.Field()
	bitcoinAddress = scrapy.Field()

    

class Thread(scrapy.Item):
	# store posts' information
	topic = scrapy.Field()
	time = scrapy.Field()
	# include every post'(include re) all content(topic, author, time, content)
	content = scrapy.Field()
	url = scrapy.Field()
	ofBoard = scrapy.Field()
	user = scrapy.Field()

class Post(Thread):
	pass
