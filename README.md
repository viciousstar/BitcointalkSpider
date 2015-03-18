BitcointalkSpider
================
##What this repo do?

- Using scrapy to crawl some dates from www.bitcointalk.org and www.bitsharestalk.org for monitoring the activities of the forum.
- And store the data which crawl from the forum.
- the lastest repo is GiveAuthentication where we add date processing and date visual display


##You need before run it

- install scrapy(refer to http://doc.scrapy.org/en/latest/intro/install.html)
- install mongodb and pymongo
- download it and switch to its catalogue 
- then edit the ``SPIDER_WORD_DIR`` which is the dir of the date stroe in settings.py 
- execute "scrapy crawl btspider"
