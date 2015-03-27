import pylab as pl
import pymongo
import datetime
import numpy as np
import os
from pymongo import MongoClient
from ..settings import SPIDER_PLOT_DIR
class plotUser(object):
    """docstring for plotUser"""
    def __init(self, clt, time):
        self.clt = clt
        self.starttime = time
    def plot(self):                    
        
        lasttime = datetime.datetime.today()
       
        datadis = {}
        dday = (lasttime - self.starttime).days
        for i in range(dday + 1):
            nowtime = self.starttime + datetime.timedelta(i)
            nowthread = clt.find({'registerDate': {'$gt': nowtime, '$lt' : nowtime + datetime.timedelta(1)}})
            count = nowthread.count()
            datadis[nowtime] = count
        sortdata = sorted(datadis.items(), key = lambda d: d[0])
        T = []
        N = []
        for key, value in sortdata:
            T.append(key)
            N.append(value)
        pl.figure(figsize = (40, 24), dpi = 160)
        pl.xticks(range(0, len(datadis)),[str(T[i].day) for i in range(0, len(datadis))])
        pl.plot(range(0, len(datadis)), N)
        pl.grid(True)
        pl.savefig(os.path.join(SPIDER_PLOT_DIR ,''.join([str(self.time.year), str(self.time.month), 'userPerDay.tif'])))
        self.configfile.close()

