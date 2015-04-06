import subprocess
import sys, os, time, datetime

def main():
    stat1 = subprocess.call(['scrapy', 'crawl', 'btthreadspider', '-s', 'JOBDIR=requestThreadData'])
    stat2 = subprocess.call(['scrapy', 'crawl', 'btuserspider', '-s', 'JOBDIR=requestUserData'])   # 

if __name__ == '__main__':
    while True:
        main()
        time.sleep(86400)   #seconds of a day
