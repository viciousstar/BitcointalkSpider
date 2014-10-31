import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BitcointalkSpider.items import User, Post, Thread
from scrapy import log

class btspider(scrapy.contrib.spiders.CrawlSpider):

	name = "btspider"
	allowed_domains = ["bitcointalk.org"]
	start_urls = ["https://bitcointalk.org/index.php"]
	'''
	some local language boards are be deny to extract, but this method may disable in the case that
	other topic or board quoat this denied topic, but this must be little, so we ignore them.
	'''
	'''
	extract by use 
	a = response.xpath("//*[@id='bodyarea']/div[4]//a[re:test(@href, 'https://bitcointalk.org/index\.php\?board=\d+\.\d+')]//@href").extract()
	b = map(str, a)
	Now I don't know how to use it in the script, I feel I was bound on the CrawlSpider!!!
	If  the struction of the board is not change, this part will work well
	'''
	denyboard = ['https://bitcointalk.org/index\.php\?board=191\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=193\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=194\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=192\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=27\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=31\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=32\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=33\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=101\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=130\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=151\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=30\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=117\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=118\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=119\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=146\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=16\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=35\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=36\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=62\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=60\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=61\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=63\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=64\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=139\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=140\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=141\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=152\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=120\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=136\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=195\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=179\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=95\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=13\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=183\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=47\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=48\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=187\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=49\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=188\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=54\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=186\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=184\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=50\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=149\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=89\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=121\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=122\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=123\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=124\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=125\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=126\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=127\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=28\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=153\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=169\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=175\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=170\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=162\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=115\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=132\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=144\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=165\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=145\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=79\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=80\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=94\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=116\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=143\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=147\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=148\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=150\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=82\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=182\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=142\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=163\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=164\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=29\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=69\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=70\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=131\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=134\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=135\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=181\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=10\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=22\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=128\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=23\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=90\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=66\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=21\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=91\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=20\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=72\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=55\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=19\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=185\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=18\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=92\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=108\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=109\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=110\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=111\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=166\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=112\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=113\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=114\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=178\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=45\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=133\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=180\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=155\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=156\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=189\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=190\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=157\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=158\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=174\.\d+', 
		          'https://bitcointalk.org/index\.php\?board=11\.\d+' 
		          ]

	rules =  (
		#rule for board
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?board=\d+\.\d+$", ), deny = (denyboard)) ),
		#rule for post, the "follow is true" is for  continuing extract
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?topic=\d+\.\d+$", ),),
			callback = "extractPost",
			follow = True),
		#rule for use
		Rule(LinkExtractor(allow = ("https://bitcointalk\.org/index\.php\?action=profile;u=\d+$", ), ),
			callback = "extractUser")
		)

	def extractPost(self, response):
		post = Thread()
		post["topic"] = response.xpath("//*[@id = 'top_subject']/text()")[0].extract().split(":")[1]
		post["content"] = []
		#every post' tr  in different board have different  @class, tr is the first character of class attribute
		#starts-with(arg1, arg2), the extract function return unicode string, but the two arg of start-with need string object
		tr =  str(response.xpath("//*[@id = 'quickModForm']/table[1]/tr[1]/@class").extract()[0])
		#every post
		smallPost = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[@class and @class = '%s']" % tr)
		# if we want tocontinue use xpath on exsit xpath, we must add "." to represent the present node
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
			post["content"].append(dict(smallpost))
		return post

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