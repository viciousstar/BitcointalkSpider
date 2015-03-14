import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient()
clt = 'bitthread'
db = client.bitdb
threadclt = db[clt]

n = 0
for thread in threadclt.find():
    try:
        thread['time'] = datetime.datetime.strptime(thread['time'][0], '%B %d, %Y, %I:%M:%S %p')
        for each in thread['content']:
            each['time'] = datetime.datetime.strptime(each['time'][0], '%B %d, %Y, %I:%M:%S %p')
        threadclt.save(thread)
    except:
        n += 1
        pass
    # print threadclt.save(thread)
print n ,'finish'        


