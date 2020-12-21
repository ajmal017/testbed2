from urllib import request
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import date, timedelta, datetime
from copy import deepcopy as dp
import json
import os

url = 'https://finance.yahoo.com/calendar/earnings?from=2020-12-13&to=2020-12-19&day=2020-12-19'
dateformat = '%Y-%m-%d'
startdate = '2011-07-20'
enddate = '2020-12-10'
weeksdate = []

d1 = datetime.strptime(startdate, dateformat)
n1 = d1.weekday()
rsd = d1 - timedelta(days=(n1 + 1))

d2 = datetime.strptime(enddate, dateformat)
n2 = d2.weekday()
red = d2 + timedelta(days=(5 - n2))

week = []
while True:
    weekday = rsd.weekday()
    strdate = rsd.strftime(dateformat)
    week.append(strdate)
    if weekday == 5:
        weeksdate.append(dp(week))
        week = []
    rsd += timedelta(days=1)
    if rsd > red:
        break

epath = r'E:\Yahoo data\Earnings'

proxy_addr = {'https': 'http://127.0.0.1:10809', 'http': 'http://127.0.0.1:10809'}
proxy = request.ProxyHandler(proxy_addr)
opener = request.build_opener(proxy, request.HTTPHandler)
request.install_opener(opener)

for wi in weeksdate:
    for di in wi:
        rurl = 'https://finance.yahoo.com/calendar/earnings?from={0}&to={1}&day={2}'.format(wi[0], wi[-1], di)
        print('下载', di)
        html = request.urlopen(rurl)
        htmldoc = html.read().decode('utf-8')
        soup = bs(htmldoc, features='lxml')
        earnings = None
        spts = soup.find_all('script')

        jtxt = ''
        for si in spts:
            txt = si.string
            if txt:
                if txt.startswith('\n(function (root)'):
                    jtxt = txt
                    break

        jh, _, jdata = jtxt.partition('root.App.main = ')
        jdata = jdata[0: -12]
        jdict = json.loads(jdata)
        try:
            earnings = jdict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
        except Exception:
            print(di, '无数据')
            continue
        if earnings:
            print('存储', di)
            savefilename = epath + os.sep + di + '.json'
            f = open(savefilename, 'w')
            json.dump(earnings, f)
            f.close()