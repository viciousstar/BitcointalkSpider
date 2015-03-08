import pylab as pl
import pymongo
import datetime
import numpy as np

from pymongo import MongoClient
client = MongoClient()
db = client.bitdb
cltname = 'bituser'
clt = db[cltname]
startyear, startmonth, startday = 2009, 11, 1
starttime = datetime.datetime(startyear, startmonth, startday)
lasttime = datetime.datetime.today()
lastyear, lastmonth, lastdat = lasttime.year, lasttime.month, lasttime.day

datadis = {}
dday = (lasttime - starttime).days
for i in range(dday + 1):
    nowtime = starttime + datetime.timedelta(i)
    nowthread = clt.find({'registerDate': {'$gt': nowtime, '$lt' : nowtime + datetime.timedelta(1)}})
    count = nowthread.count()
    datadis[nowtime] = count

sortdata = sorted(datadis.items(), key = lambda d: d[0])

T = []
N = []
for key, value in sortdata:
    T.append(key.isoformat())
    N.append(value)


pl.figure(figsize = (40, 24), dpi = 160)
pl.xticks(range(0, len(datadis), 120),[T[i] for i in range(0, len(datadis), 120)])
pl.plot(range(0, len(datadis)), N)
pl.grid(True)
pl.savefig('/home/thl/Pictures/userPerDay.tif')


