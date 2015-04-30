BitcointalkSpider
================
## Overview

BitcointalkSpider is a web crawler targeting at crawling down all the data of [Bitcoin Forum](http://www.bitcointalk.org). It is based on [Scrapy](http://www.scrapy.org). We hope this data can enable us to analyse the relationship between user activeness on Bitcoin Forum and trends of Bitcoin price.

## How to run it

1. install scrapy (refer to http://doc.scrapy.org/en/latest/intro/install.html)
2. install mongodb and pymongo
4. run mongod
3. download it, switch to its folder in the terminal, and execute 'scrapy crawl btthreadspider -s JOBDIR=requestThreadData' or 'scrapy crawl btthreadspider -s JOBDIR=requestThreadData' or 'python start.py'

FoOTOo Lab 2014-2015

# 配置文件
##爬虫配置文件 `BitcointalkSpider/spiders/setting.py`
- SPIDER_WORK_DIR 抓取数据存储位置 
- DOWNLOADER_MIDDLEWARES 下载中间件
- ITEM_PIPELINES 输出json文件中间件


# 数据文件
## 数据格式
###user
{
  "name" : [
    "SheriffWoody"                  
`列表，字符串`
  ],
  "gender" : [ ],                            
`列表， 字符串，可能为空， Male， Female`
  "age" : [
    "N/A" 
`列表， 字符串， 可能为 N/A， 或者数字`
  ],
  "posts" : [
    "5" 
`列表， 字符串， 正整数`
  ],
  "lastDate" : [
    "May 17, 2011, 06:43:45 PM"    
`列表， 字符串， "%B %d, %Y, %I:%M:%S %p"， 或者 [ "Today", " at 03:19:13 PM" ]`
  ],
  "activity" : [
    "5"
`列表， 字符串， 正整数`
  ],
  "bitcoinAddress" : [ ],
`列表，字符串， 为包含bitcoin地址的复杂字符串`
  "position" : [
    "Newbie"
`列表，字符串， 分类 Newbie Legendary Jr.member Member Full merber Sr. Membe Hero Member  etc.`
  ],
  "registerDate" : [
    "March 05, 2010, 01:57:46 AM"
`列表， 字符串， "%B %d, %Y, %I:%M:%S %p"， 或者 [ "Today", " at 03:19:13 PM" ]`
  ],
  "Email" : [
    "hidden"
`列表， 字符串， hidder 或者 邮件地址`
  ]
}
###thread
{
  "topic": " ..  (Read 1832 times)\n\t\t\t\t",
`字符串`
  "ofBoard": [
    "Bitcoin Forum",
    "Economy",
    "Trading Discussion",
    ".."
  ],
`列表 多元素字符串`
  "url": "https://bitcointalk.org/index.php?topic=151196.0",
 `字符串`
 "content": [
    {
      "topic": [
        ".."
      ],
      "content": [
        ".."
      ],
      "user": [
        "Fabrizio89"
      ],
      "time": []
    },
    {
      "topic": [
        "Re: ASIC miner shares."
      ],
      "content": [
        "Just a minor thing: You expose yourself to more risk if you don't trade the shares directly. burnside is trustworthy in my opinion, but it is still risk, and there are future management fees, and you need to judge if that is worth the easier share purchases, purchasing of smaller amounts or greater liquidity, etc. "
      ],
      "user": [
        "$username"
      ],
      "time": [
        "March 18, 2013, 09:58:23 AM"
      ]
    }
  ],
`列表 包含很多和主thread相同的结构，但是缺少url`
  "user": [
    "Fabrizio89"
  ],
`列表 元素为单元素 字符串`
  "time": []
`列表， 字符串， "%B %d, %Y, %I:%M:%S %p"`
}
###数据库中数据格式
- 二者的时间都转换 成了 ``ISODate("2015-04-04T23:08:27Z")``
- 增加了整数类型的year， month， day


##数据统计
### 用户数据
对于网站活跃度来说，目前用到的用户数据比较有用的有 


- registerDate：某一短时间内新注册的用户数量，`需要统计每天的新增用户数`
- positions： 等级可能对与整体活跃度的所占的权重有所不同


### 帖子数据
- 整个论坛某段时间（日， 周， 月。。。）内的所有新增帖子
- 相比所有新增帖子而言，或许所有新回复更能体现网站的活跃度
- 分别统计每个版块的活跃度，每个板块代表的意义不尽相同



#技术架构
整个项目目前没有跳出scrapy框架，具体scrapy工作细节请参考：[Architecture overview](http://doc.scrapy.org/en/latest/topics/architecture.html).


##爬虫部分介绍
###btthreadspider.py
- `class btthreadspider(scrapy.contrib.spiders.Spider)`：完全继承自scrapy自带爬虫类(额外知识，可能需要了解一下xpath) spider
主要负责thread的简单提取，和抓取内容的简单处理。将抓取到的内容以scrapy.item 返回。
###btuserspider.py
- `class btuserspider(scrapy.contrib.spiders.Spider)`：完全继承自scrapy自带爬虫类(额外知识，可能需要了解一下xpath) spider
主要负责user的简单提取，和抓取内容的简单处理。将抓取到的内容以scrapy.item 返回


### item.py
- `class  User(scrapy.Item)` ：scrapy.item 类，对字典的包装。


### pipeline.py
- `class JsonWithEncodingPipeline(object):` 对爬虫返回的item类进行处理，写入json文件，并且存入数据库。参考：[item pipeline](http://doc.scrapy.org/en/latest/topics/item-pipeline.html)

### filterurl.py
- `class FilterurlExtension(object)`: 完全自己实现的一个类，但是其实现方式要遵守一定的规范，主要功能是记录爬虫的启动，关闭时间，方便增量爬取。
参考：[extensions](http://doc.scrapy.org/en/latest/topics/extensions.html)

###retryMiddleware.py
- ``class MyRetryMiddleware(RetryMiddleware):`` 区分url是否为网站的入口主节点，采取不同的retry策略。
- ``def process_response(self, request, response, spider):`` 检测网络状况，是否需要停止爬虫。

###start.py
- 自动长久启动爬虫

#开发工具
- scrapy
- mongodb
- pylab
