import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BitcointalkSpider.items import User, Post
from scrapy import log

class btspider(scrapy.contrib.spiders.CrawlSpider):

	name = "btspider"
	allowed_domains = ["bitcointalk.org"]
	start_urls = ["https://bitcointalk.org/index.php"]

	rules =  (
		#rule for board
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?board=\d+\.\d+", ) ) ),
		#rule for post, the "follow is true" is for  continuing extract
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?topic=\d+\.\d", ), ),
			callback = "extractPost",
			follow = True),
		#rule for use
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?action=profile;u=\d+", ), ),
			callback = "extractUser")
		)

	def extractPost(self, response):
		post = Post()
		post["topic"] = response.xpath("//*[@id = 'top_subject']/text()")[0].extract().split(":")[1]
		post["content"] = []
		#every post' tr  in different board have different  @class, tr is the first character of class attribute
		#starts-with(arg1, arg2), the extract function return unicode string, but the two arg of start-with need string object
		tr =  str(response.xpath("//*[@id = 'quickModForm']/table[1]/tr[1]/@class").extract()[0])
		#every post
		smallPost = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[@class and @class = '%s']" % tr)
		i# if we want to continue use xpath on exsit xpath, we must add "." to represent the present node
		post["user"] = smallPost[0].xpath("(.//a[@href])[1]/text()").extract()
		post["time"] = smallPost[0].xpath("(.//div[@class = 'smalltext'])[2]/text()").extract()
		post["url"] = response.url
		boardlist = response.xpath("//a[@class = 'nav']/text()").extract()
		#every is a of
		#lenBoardlist //a[@class = 'nav']/text() occur two postion (head and tail)
		lenBoardlist = len(boardlist) / 2
		post["ofBoard"] = [boardlist[x] for x in range(0, lenBoardlist)]
		#store every post partly by loop
		for  everyPost in smallPost:			
			smallpost = Post()
			smallpost["user"] = everyPost.xpath("(.//a[@href])[1]/text()").extract()
			smallpost["topic"] = everyPost.xpath(".//*[@class = 'subject']/a/text()").extract()
			smallpost["time"] =  everyPost.xpath("(.//div[@class = 'smalltext'])[2]/text()").extract()
			smallpost["content"] = everyPost.xpath(".//div[@class = 'post']/text()").extract()
			post["content"].append(smallPost)
		return post

	def extractUser(self, response):
		user = User()
		userinfo = response.xpath("//table[@align = 'center' and @cellpadding = '4']//text()").extract()
		# extract every info form list of  userinfo
		list_userinfo = enumerate(userinfo)
		for index, info in list_userinfo:
			#avoid list out of index
			try:
				foo = list_userinfo[index + 2][1].strip()
				if foo != "":
					if  info.find("Name") != -1:
						user["name"] = foo
						continue
					if  info.find("Posts") != -1:
						user["post"] = foo
						continue
					if  info.find("Activity") != -1:
						user["activity"] = foo
						continue
					if  info.find("Position") != -1:
						user["positon"] = foo
						continue
					if  info.find("Date Refistered") != -1:
						user["registerData"] = foo
						continue
					if  info.find("Last Active") != -1:
						user["lastData"] = foo
						continue
					if  info.find("Email: ") != -1:
						user["Email"] = foo
						continue
					if  info.find("Gender") != -1:
						user["gender"] = foo
						continue
					if  info.find("Age") != -1:
						user["age"] = foo
						continue
					if  info.find("") != -1:
						user["bitcoinAddress"] = foo
						continue
			except:
				log.msg("out of index!!!")
				break
		return user