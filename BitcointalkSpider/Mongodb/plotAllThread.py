# coding: utf-8
import pylab as pl
import pymongo
from pymongo import MongoClient
import datetime
import ConfigParser
# import numpy as np    May not use
class plotThread:
    def __init(self, clt):
        self.clt = clt
        self.configfile = open(os.path.join(SPIDER_PRO_DIR, 'config.cfg'), 'r')
        config = ConfigParser.ConfigParser()
        config.readfp(self.configfile)
        self.time = config.get('SPIDER', 'start_time')
        self.starttime = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
    def plot(self):
        lasttime = datetime.datetime.today()                #should be the time of crawl finish
    
        datadis = {}
        dday = (lasttime - self.starttime).days
        for i in range(dday + 1):
            nowtime = self.starttime + datetime.timedelta(i)
            nowthread = self.clt.find({'time': {'$gt': nowtime, '$lt' : nowtime + datetime.timedelta(1)}})
            count = nowthread.count()                       #the board of the thread may be distincted
            datadis[nowtime] = count

        sortdata = sorted(datadis.items(), key = lambda d: d[0])
        T = []
        N = []
        for key, value in sortdata:
            T.append(key)                       #xtick should be simplify
            N.append(value)
        pl.figure(figsize = (40, 24), dpi = 80)             #the size of figure should be write in config.file
        pl.xticks(range(0, len(datadis)),[str(T[i].day) for i in range(0, len(datadis))])        #the time gap should be config
        pl.plot(range(0, len(datadis)), N)
        pl.grid(True)                                        #num of thread should appear in yticks
        pl.savefig('/home/thl/Pictures/' + str(self.time.year) + str(self.time.month) + 'ThreadPerDay.pdf')    #config
        self.configfile.close()