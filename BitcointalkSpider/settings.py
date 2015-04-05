# -*- coding: utf-8 -*-
import os

BOT_NAME = 'BitcointalkSpider'
#some info file use : stat.info
SPIDER_PRO_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

#the dir of data store
SPIDER_DATA_DIR = os.path.join(SPIDER_PRO_DIR, 'Data')
SPIDER_PLOT_DIR = os.path.join(SPIDER_PRO_DIR, 'Plot')
SPIDER_RETRYURL_DIR = os.path.join(SPIDER_PRO_DIR, 'RetryUrl') 
# JOBDIR = os.path.join(SPIDER_PRO_DIR, 'requestData')
SPIDER_MODULES = ['BitcointalkSpider.spiders']
NEWSPIDER_MODULE = 'BitcointalkSpider.spiders'
RETRY_ENABLED = True
RETRY_MAIN_TIMES = 10
COOKIES_ENABLED = True
# COOKIES_DEBUG = True
DOWNLOAD_TIMEOUT = 15
DOWNLOAD_DELAY = 1
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(SPIDER_PRO_DIR, "scrapy.log")
CONCURRENT_REQUESTS_PER_DOMAIN = 300
CONCURRENT_REQUESTS = 300
#depth priority
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'
#output item as json
ITEM_PIPELINES = {'BitcointalkSpider.pipelines.JsonWithEncodingPipeline' : 800}
#recode time info of spider and filter url according to time
EXTENSIONS = {
    'BitcointalkSpider.filterurl.FilterurlExtension' : 1
}
#DUPEFILTER_CLASS = 'BitcointalkSpider.filterurl.SaveRequestSeen'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': None,
    'BitcointalkSpider.retryMiddleware.MyRetryMiddleware': 500
}

# stop spider if the 
MAX_EXCEPTION_PER_HOUR = 100
# second of SUSPEND
SUSPEND_TIME = 3600