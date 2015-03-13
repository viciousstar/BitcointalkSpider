import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BitcointalkSpider.items import User, Post, Thread
from scrapy import log


class btthreadspider(scrapy.contrib.spiders.CrawlSpider):

	name = "btthreadspider"
	allowed_domains = ["bitcointalk.org"]
	start_urls = ["https://bitcointalk.org/index.php"]

	rules =  (
		#rule for board
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?board=\d+\.\d+$", )),
		#rule for post, the "follow is true" is for  continuing extract
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?topic=\d+\.\d+$", )),
			callback = "extractPost",
			follow = True),
		)
		)

	def extractPost(self, response):
		post = Thread()
		post["topic"] = response.xpath("//*[@id = 'top_subject']/text()")[0].extract().split(":")[1]
		post["content"] = []
		tr =  str(response.xpath("//*[@id = 'quickModForm']/table[1]/tr[1]/@class").extract()[0])
		#every post
		smallPost = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[@class and @class = '%s']" % tr)
		# if we want tocontinue use xpath on exsit xpath, we must add "." to represent the present node
		post["user"] = smallPost[0].xpath("(.//a[@href])[1]/text()").extract()
		post["time"] = smallPost[0].xpath("(.//div[@class = 'smalltext'])[2]/text()").extract()
		post["url"] = response.url
		boardlist = response.xpath("//a[@class = 'nav']/text()").extract()
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
			post["content"].append(dict(smallpost))
		return post





class btuserspider(scrapy.contrib.spiders.CrawlSpider):
	name = "btuserspider"
	allowed_domains = ["bitcointalk.org"]
	start_urls = ["https://bitcointalk.org/index.php?action=mlist;sort=registered;start=0;desc"]
	
	rules =  (
		#rule for use
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?action=profile;u=\d+$", ), ),
			callback = "extractUser"),
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?action=mlist;sort=registered;start=\d+;desc")))
		
		)			#may add renz

	def parse_start_url(self, response):
		open('login.html', 'w').write(response.body)
		rsq = scrapy.FormRequest.from_response(
			response,
			formdata={'user': 'vicious_starr%%40163.com', 'passwrd': 'qwer1234'},
			callback=self.after_login
		)
		print rsq.headers
		print  '\n\n\n\n\n\n'
		return rsq
	
	def after_login(self, response):
		open('after_login.html', 'w').write(response.body)
		rsq = scrapy.Request(url = 'https://bitcointalk.org/index.php?action=login2%3bsa=check%3bmember=379410', headers = {'Host': 'bitcointalk.org',
                'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:36.0) Gecko/20100101 Firefox/36.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                #'Cookie':  'SMFCookie129=a%3A4%3A%7Bi%3A0%3Bs%3A6%3A%22379410%22%3Bi%3A1%3Bs%3A40%3A%2269f88edb7ee63f5b54f4dfdd532d4cd7a8b6bd29%22%3Bi%3A2%3Bi%3A1426168224%3Bi%3A3%3Bi%3A0%3B%7D',
                'Connection': 'keep-alive',
                'If-Modified-Since': 'Thu, 12 Mar 2015 08:52:12 GMT',
                'Cache-Control': 'max-age=0'})
		print rsq.headers
		print  '\n\n\n\n\n\n'
		return rsq
	def after_login2(self, response):
		open('after_login2.html', 'w').write(response.body)

	def extractUser(self, response):
		user = User()
		userinfo = response.xpath("//table[@border = '0'  and @cellpadding = '2']/tr")
		# extract every info form list of  userinfo
		for character in userinfo:
			text = filter(unicode.strip, character.xpath(".//text()").extract())
			if  text != []:
				lenText = len(text)
				textname = text[0]
				text.pop(0)
				if  textname.find("Name") != -1:
					if len > 1:
						user["name"] = text
					else:
						user["name"] = None
					continue
				if  textname.find("Posts") != -1:
					if len > 1:
						user["posts"] = text
					else:
						user["posts"] = None
					continue
				if  textname.find("Activity") != -1:
					if len > 1:
						user["activity"] = text
					else:
						user["activity"] = None
					continue
				if  textname.find("Position") != -1:
					if len > 1:
						user["position"] = text
					else:
						user["position"] = None
					continue
				if  textname.find("Date Registered") != -1:
					if len > 1:
						user["registerDate"] = text
					else:
						user["registerDate"] = None
					continue
				if  textname.find("Last Active") != -1:
					if len > 1:
						user["lastDate"] = text
					else:
						user["lastDate"] = None
					continue
				if  textname.find("Email: ") != -1:
					if len > 1:
						user["Email"] = text
					else:
						user["Email"] = None
					continue
				if  textname.find("Gender") != -1:
					if len > 1:
						user["gender"] = text
					else:
						user["gender"] = None
					continue
				if  textname.find("Age") != -1:
					if len > 1:
						user["age"] = text
					else:
						user["age"] = None
					continue
				if  textname.find("Signature") != -1:
					if len > 1:
						user["bitcoinAddress"] = text
					else:
						user["bitcoinAddress"] = None
					continue
			else:
				continue
		return user