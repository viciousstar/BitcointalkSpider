# -*- coding: utf-8 -*-

# Scrapy settings for BitcointalkSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'BitcointalkSpider'
SPIDER_WORK_DIR = '/home/thl/project/BitcointalkSpider/Data'
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
LOG_LEVEL = "DEBUG"
# turn up speed of spider
#LOG_FILE = "scrapy.log"
CONCURRENT_REQUESTS_PER_DOMAIN = 300
CONCURRENT_REQUESTS = 300
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#取消默认的useragent,使用新的useragent
DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : None,
        'BitcointalkSpider.rotate_useragent.RotateUserAgentMiddleware' :400
    }

ITEM_PIPELINES = ['BitcointalkSpider.pipelines.JsonWithEncodingPipeline']