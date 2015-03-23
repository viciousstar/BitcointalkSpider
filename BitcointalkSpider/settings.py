# -*- coding: utf-8 -*-
import os

BOT_NAME = 'BitcointalkSpider'
#the dir of data store
SPIDER_PRO_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

SPIDER_WORK_DIR = os.path.join(SPIDER_PRO_DIR, 'Data')
#some info file use : stat.info

SPIDER_MODULES = ['BitcointalkSpider.spiders']
NEWSPIDER_MODULE = 'BitcointalkSpider.spiders'
RETRY_ENABLED = False
COOKIES_ENABLED = True
COOKIES_DEBUG = True
DOWNLOAD_TIMEOUT = 15
DOWNLOAD_DELAY = 1
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(SPIDER_PRO_DIR, "scrapy.log")
CONCURRENT_REQUESTS_PER_DOMAIN = 300
CONCURRENT_REQUESTS = 300
#output item as json
ITEM_PIPELINES = ['BitcointalkSpider.pipelines.JsonWithEncodingPipeline']
#recode time info of spider and filter url according to time
EXTENSIONS = {
    'BitcointalkSpider.filterurl.FilterurlExtension' : 500
}
DUPEFILTER_CLASS = 'BitcointalkSpider.filterurl.SaveRequestSeen'