import datetime
import pymongo
from pymongo import MongoClient

client = MongoClient()
clt = 'bituser'
db = client.bitdb
userclt = db[clt]

'''
{u'Email': [u'hidden'],
 u'_id': ObjectId('54f96b555fb95427fe42fd11'),
 u'activity': [u'5'],
 u'age': [u'N/A'],
 u'bitcoinAddress': [],
 u'gender': [],
 u'lastDate': datetime.datetime(2011, 5, 17, 18, 43, 45),
 u'name': [u'SheriffWoody'],
 u'position': [u'Newbie'],
 u'posts': [u'5'],
 u'registerDate': [u'March 05, 2010, 01:57:46 AM']}
 '''
for user in userclt.find():
    try:
        user['lastDate'] = datetime.datetime.strptime(user['lastDate'][0], '%B %d, %Y, %I:%M:%S %p')
        user['registerDate'] = datetime.datetime.strptime(user['registerDate'][0], '%B %d, %Y, %I:%M:%S %p')
        user['activity'] = int(user['activity'][0]) 
        user['posts'] = int(user['posts'][0]) 
    except:
        pass
    userclt.save(user)
        


