# coding: utf-8
import pylab as pl
import pymongo
from pymongo import MongoClient
import datetime
import os
import ConfigParser
from ..settings import SPIDER_PLOT_DIR

# import numpy as np    May not use
class plotThread:
    def __init(self, clt, time):
        self.clt = clt
        self.starttime = time
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
        pl.savefig(os.path.join(SPIDER_PLOT_DIR ,''.join([str(self.time.year), str(self.time.month), 'threadPerDay.tif'])))
        self.configfile.close()