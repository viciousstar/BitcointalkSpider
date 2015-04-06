import subprocess
import sys, os, time, datetime

def main():
    stat = subprocess.call(['scrapy', 'crawl', 'btthreadspider', '-s', 'JOBDIR=requestData'])

    if stat == 0:
        f.write(datetime.datetime.today().isoformat() + '   Scrapy Finish.\n')
        print 'Success'
    else:
        f.write(datetime.datetime.today().isoformat() + '   Scrapy breakdown.\n')
        print 'Fail'
    




if __name__ == '__main__':
    while True:
        main()
        time.sleep(86400)   #seconds of a day
