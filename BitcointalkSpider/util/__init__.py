import os
from datetime import datetime

def timeFormat(time):
    try:
        if time.find('at'):
            today = datetime.today()
            time = datetime.strptime(time.strip(), 'at %I:%M:%S %p')
            time = time.replace(today.year, today.month, today.day)
        else:
            time = datetime.strptime(time.strip(), "%B %d, %Y, %I:%M:%S %p")
        return time
    except:
        return None

def incAttr(dct, s):
    if s in dct:
        dct[s] = dct[s] + 1
    else:
        dct[s] = 0

def creatPath(*args):
    for s in args:
        if os.path.exists(s):
            pass
        else:
            os.makedirs(s)
