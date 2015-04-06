from pymongo import MongoClient
client = MongoClient()
db = client.bitdb
threadclt = db.bitthread
urldict = {}
for thread in threadclt.find():
    try:
        one, two = thread['url'].split('=')[1].split('.')
        if urldict.has_key(one):
            urldict[one].append(two)
        else:
            urldict[one] = []
            urldict[one].append(two)
    except:
        print thread['url']
for key in urldict:
    try:
        urldict[key].remove('0')
    except:
        pass
n = 0
for key,value in urldict.iteritems():
    content = []
    for suf in value:
        url = 'https://bitcointalk.org/index.php?topic=' + key + '.' + suf
        try:
            content.extend(threadclt.find({'url': url})[0]['content'])
            threadclt.remove({'url': url})
        except:
             pass
    suurl = 'https://bitcointalk.org/index.php?topic=' + key + '.0'
    
    try:
        content.extend(threadclt.find({'url': suurl})[0]['content'])
        threadclt.update({'url': suurl},
                     {
            '$set': {
                'content' :  content
                }})
    except:
        n += 1
        print suurl
print 'finish'