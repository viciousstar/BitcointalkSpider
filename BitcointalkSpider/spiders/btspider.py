import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BitcointalkSpider.items import User, Post, Thread
from scrapy import log

class btspider(scrapy.contrib.spiders.CrawlSpider):

	name = "btspider"
	allowed_domains = ["bitsharestalk.org"]
	start_urls = ["https://bitsharestalk.org/index\.php"]
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
'''
	rules =  (
		Rule(LinkExtractor(allow = ("https://bitsharestalk\.org/index\.php\?\S*board=\d+\.\d+$", )), process_links = 'link_filtering'),
		Rule(LinkExtractor(allow = ("https://bitsharestalk\.org/index\.php\?\S*topic=\d+\.\d+$", ),),
			callback = "extractPost",
			follow = True, process_links = 'link_filtering'),
		Rule(LinkExtractor(allow = ("https://bitsharestalk\.org/index\.php\?\S*action=profile;u=\d+$", ),),
			callback = "extractUser", process_links = 'link_filtering')
		)
	def link_filtering(self, links):
	        	ret = []
	        	for link in links:
	        		url = link.url
	        		urlfirst, urllast = url.split("?")
	        		if urllast:
	        			link.url = urlfirst + "?" + urllast.split("&")[1]
	        	return links
	def extractPost(self, response):
		post = Thread()
		post["topic"] =  response.xpath("//*[@id='forumposts']/div/h3/text()").extract()[-1].split(":")[-1]
		post["content"] = []
		smallPost = response.xpath("//div[@class='post_wrapper']")
		post["user"] = smallPost[0].xpath("./div[@class='poster']/h4/a/text()").extract()
		post["time"] = smallPost[0].xpath("./div[@class='postarea']//div[@class='smalltext']/text()")[-1].extract()
		post["url"] = response.url
		boardlist = response.xpath("//div[@class='navigate_section']//a//text()").extract()
		post["ofBoard"] = boardlist
		for  everyPost in smallPost:			
			smallpost = Post()
			smallpost["user"] = everyPost.xpath("./div[@class='poster']/h4/a/text()").extract()
			smallpost["topic"] = everyPost.xpath("//*[@id='forumposts']/div/h3/text()").extract()[-1].split(":")[-1]
			smallpost["time"] =  everyPost.xpath("./div[@class='postarea']//div[@class='smalltext']/text()")[-1].extract()
			smallpost["content"] = everyPost.xpath("./div[@class='postarea']/div[@class='post']//text()").extract()
			post["content"].append(dict(smallpost))
		return post

	def extractUser(self, response):
		user = User()
		user["name"] =  response.xpath("//div[@class='username']//text()")[0].extract() 
		userinfo = filter(unicode.strip, response.xpath("//*[@id='detailedinfo']/div[@class='windowbg2']/div[@class='content']//text()").extract())
		if userinfo:
			for text in range(0, len(userinfo), 2):
				if userinfo[text].startswith("Posts"):
					user["posts"] = userinfo[text + 1]
					continue
				elif userinfo[text].startswith("Age"):
					user["age"] = userinfo[text + 1]
					continue
				elif userinfo[text].startswith("Last Active:"):
					if userinfo[text + 1] = "Today"
					user["Last Active:"] = [userinfo[text + 1], userinfo[text + 2]
					text += 1
					continue
				elif userinfo[text].startswith("Date Registered"):
					user["registerData"] = userinfo[text + 1]
					continue
				elif userinfo[text].startswith("Signature:"):
					user["bitcoinAddress"] = userinfo[text + 1]
					continue
		return user
