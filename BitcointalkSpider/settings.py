# -*- coding: utf-8 -*-

# Scrapy settings for BitcointalkSpider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'BitcointalkSpider'

SPIDER_MODULES = ['BitcointalkSpider.spiders']
NEWSPIDER_MODULE = 'BitcointalkSpider.spiders'
# retry
RETRY_ENABLED = False
# cookie, we don't need cookies in this website
COOKIES_ENABLED = False
# this time have to reset
DOWNLOAD_TIMEOUT = 50

DOWNLOAD_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'BitcointalkSpider (+http://www.yourdomain.com)'
