# coding: utf-8
import pylab as pl
import pymongo
from pymongo import MongoClient
import datetime
# import numpy as np    May not use

client = MongoClient()
db = client.bitdb
cltname = 'bitthread'
clt = db[cltname]
startyear, startmonth, startday = 2013, 11, 1       #need write in config.file
starttime = datetime.datetime(startyear, startmonth, startday)
lasttime = datetime.datetime.today()                #should be the time of crawl finish
lastyear, lastmonth, lastdat = lasttime.year, lasttime.month, lasttime.day

datadis = {}
dday = (lasttime - starttime).days
for i in range(dday + 1):
    nowtime = starttime + datetime.timedelta(i)
    nowthread = clt.find({'time': {'$gt': nowtime, '$lt' : nowtime + datetime.timedelta(1)}})
    count = nowthread.count()                       #the board of the thread may be distincted
    datadis[nowtime] = count



sortdata = sorted(datadis.items(), key = lambda d: d[0])

T = []
N = []
for key, value in sortdata:
    T.append(key.isoformat())                       #xtick should be simplify
    N.append(value)
pl.figure(figsize = (40, 24), dpi = 80)             #the size of figure should be write in config.file
pl.xticks(range(0, len(datadis), 60),[T[i] for i in range(0, len(datadis), 60)])        #the time gap should be config
pl.plot(range(0, len(datadis)), N)
pl.grid(True)                                        #num of thread should appear in yticks
pl.savefig('/home/thl/Pictures/ThreadPerDay.pdf')    #config
