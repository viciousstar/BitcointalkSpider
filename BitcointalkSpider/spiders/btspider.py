import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from BitcointalkSpider.items import User, Post

class btspider(scrapy.contrib.spiders.CrawlSpider):

	name = "btspider"
	allowed_domains = ["bitcointalk.org"]
	start_url = ["https://bitcointalk.org/index.php"]

	rules =  (

		Rules(LinkExtractor(allow = ("https://bitcointalk.org/index.php?board=\d+.\d+"))),

		Rules(LinkExtractor(allow = ("https://bitcointalk.org/index.php?topic=\d+.\d"),
			callback = extractorPost),
			follow = True),





		)

	def extractorPost(self, response):
		post = Post()
		post.topic = response.xpath("//*[id = "top_subject"]/text()").extract().spilt(":")[1]
		post.content = []
		preTr =  response.xpath("//*[@id = 'quickModForm']/table[1]/tr[1]/@class").extract()[0][0]
		#every post
		smallPost = response.xpath("//*[@id = 'quickModForm']/table[1]//tr[start-with(@class, preTr)]")
		post.user = smallPost[0].xpath("//a[1]/text()").extract()
		post.time = smallPost[0].xpath("//*[@class = 'smalltext']/text()").extract()
		post.url = response.url
		boardlist = response.xpath("//div[@class = 'nav'][1]//text")
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
