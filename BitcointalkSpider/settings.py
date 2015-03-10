# -*- coding: utf-8 -*-

BOT_NAME = 'BitcointalkSpider'
SPIDER_WORK_DIR = '/home/thl/github/BitcointalkSpider/Data'
SPIDER_MODULES = ['BitcointalkSpider.spiders']
NEWSPIDER_MODULE = 'BitcointalkSpider.spiders'
# retry
RETRY_ENABLED = False
# cookie, we don't need cookies in this website
COOKIES_ENABLED = False
# this time have to reset
DOWNLOAD_TIMEOUT = 15

DOWNLOAD_DELAY = 1
# get out of debug stage
LOG_LEVEL = "INFO"
# turn up speed of spider
#LOG_FILE = "scrapy.log"
CONCURRENT_REQUESTS_PER_DOMAIN = 300
CONCURRENT_REQUESTS = 300
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#取消默认的useragent,使用新的useragent
# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
#         'BitcointalkSpider.rotate_useragent.RotateUserAgentMiddleware' :400
#     }

ITEM_PIPELINES = ['BitcointalkSpider.pipelines.JsonWithEncodingPipeline']

EXTENSIONS = {
    'BitcointalkSpider.filterurl.FilterurlExtension' : 500
}

DUPEFILTER_CLASS = 'BitcointalkSpider.filterurl.SaveRequsetSeen'