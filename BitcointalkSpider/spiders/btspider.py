import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BitcointalkSpider.items import User, Post
import scrapy.log

class btspider(scrapy.contrib.spiders.CrawlSpider):

	name = "btspider"
	allowed_domains = ["bitcointalk.org"]
	start_url = ["https://bitcointalk.org/index.php"]

	rules =  (
		#rule for board
		Rules(LinkExtractor(allow = ("https://bitcointalk.org/index.php?board=\d+.\d+"))),
		#rule for post, the "follow is true" is for  continuing extract
		Rules(LinkExtractor(allow = ("https://bitcointalk.org/index.php?topic=\d+.\d"),
			callback = extractorPost),
			follow = True),
		#rule for use
		Rules(LinkExtractor(allow = ("https://bitcointalk.org/index.php?action=profile;u=\d+"), 
			callback = extractUser)),




		)

	def extractorPost(self, response):
		post = Post()
		post.topic = response.xpath("//*[id = "top_subject"]/text()").extract().spilt(":")[1]
		post.content = []
		#every post' tr  in different board have different  @class, pretr is the first character of class attribute
		preTr =  response.xpath("//*[@id = 'quickModForm']/table[1]/tr[1]/@class").extract()[0][0]
		#every post
		smallPost = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[start-with(@class, preTr)]")
		post.user = smallPost[0].xpath("//a[1]/text()").extract()
		post.time = smallPost[0].xpath("//*[@class = 'smalltext']/text()").extract()
		post.url = response.url
		boardlist = response.xpath("//div[@class = 'nav'][1]//text")
		#every is a of
		post.ofBoard = [boardlist[0], boardlist[2], boardlist[4], boardlist[8]]
		#store every post partly by loop
		for  everyPost in smallPost:			
			smallpost = Post()
			smallpost.user = everyPost.xpath("//a[1]/text()").extract()
			smallpost.topic = everyPost.xpath("//*[@class = 'subject']/a/text()").extract()
			smallpost.time =  everyPost.xpath("//*[@class = 'smalltext']/text()").extract()
			smallpost.content = everyPost.xpath("//div[@class = 'post']/text()").extract()
			post.append(smallPost)

		return post

	def extractorUser(self, response):
		user = User()
		userinfo = response.xpath("//table[@align = 'center' and @cellpadding = '4']//text()").extract()
		# extract every info form list of  userinfo
		list_userinfo = enumerate(userinfo)
		for index, info in list_userinfo:
			#avoid list out of index
			try:
				if  info.find("Name: ") != -1 and (name = list_userinfo[index + 2][1].strip()) != '':
					user.name = name
				if  info.find("Posts") != -1 and (post = list_userinfo[index + 2][1].strip()) != '':
					user.post = post
				if  info.find("Activity") != -1 and (activity = list_userinfo[index + 2][1].strip()) != '':
					user.activity = activity
				if  info.find("Position") != -1 and (positon = list_userinfo[index + 2][1].strip()) != '':
					user.positon = positon
				if  info.find("Date Refistered") != -1 and (registerData = list_userinfo[index + 2][1].strip()) != '':
					user.registerData = registerData
				if  info.find("Last Active") != -1 and (lastData = list_userinfo[index + 2][1].strip()) != '':
					user.lastData = lastData
				if  info.find("Email: ") != -1 and (Email = list_userinfo[index + 2][1].strip()) != '':
					user.Email = Email
				if  info.find("Gender") != -1 and (gender = list_userinfo[index + 2][1].strip()) != '':
					user.gender = gender
				if  info.find("Age") != -1 and (age = list_userinfo[index + 2][1].strip()) != '':
					user.age = age
				if  info.find("") != -1 and (bitcoinAddress = list_userinfo[index + 2][1].strip()) != '':
					user.bitcoinAddress = bitcoinAddress
			except:
				log.message("out of index!!!")
				break
		return user