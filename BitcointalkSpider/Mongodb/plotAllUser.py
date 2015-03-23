import pylab as pl
import pymongo
import datetime
import numpy as np
from pymongo import MongoClient

class plotUser(object):
    """docstring for plotUser"""
    def __init(self, clt):
        self.clt = clt
        self.configfile = open(os.path.join(SPIDER_PRO_DIR, 'config.cfg'), 'r')
        config = ConfigParser.ConfigParser()
        config.readfp(self.configfile)
        self.time = config.get('SPIDER', 'start_time')
        self.starttime = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
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
        pl.savefig('/home/thl/Pictures/' + str(self.time.year) + str(self.time.month) + 'userPerDay.tif')
        self.configfile.close()

