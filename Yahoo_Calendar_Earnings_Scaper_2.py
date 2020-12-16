from urllib import request
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import date, timedelta, datetime
from copy import deepcopy as dp
import json
import os

url = 'https://finance.yahoo.com/calendar/earnings?from=2011-07-17&to=2011-07-23&day=2011-07-18&symbol=IBM&offset=0&size=100'
epath = r'E:\Yahoo data\Earnings 2'

proxy_addr = {'https': 'http://127.0.0.1:10809', 'http': 'http://127.0.0.1:10809'}
proxy = request.ProxyHandler(proxy_addr)
opener = request.build_opener(proxy, request.HTTPHandler)
request.install_opener(opener)


def get_yahoo_earnings_100(symbol: str, offset: int):
    rurl = 'https://finance.yahoo.com/calendar/earnings?from=2011-07-17&to=2011-07-23&day=2011-07-18&symbol={}&offset={}&size=100'.format(symbol.upper(), offset * 100)
    print('下载{}数据{}'.format(symbol.upper(), offset))
    html = request.urlopen(rurl)
    htmldoc = html.read().decode('utf-8')
    soup = bs(htmldoc, features='lxml')
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

    earnings = None
    try:
        earnings = jdict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
    except Exception:
        print('无数据')

    return earnings


def get_yahoo_earnings(symbol: str):
    es = []
    offset = 0
    while True:
        e = get_yahoo_earnings_100(symbol, offset)
        offset += 1
        if e:
            es += e
            if len(e) < 100:
                break
        else:
            break
    return es


if __name__ == '__main__':
    # spath = r'E:\newdata\OCC data\Adj Data\202006-Full-Y.csv'
    # sdf = pd.read_csv(spath)
    symbols = [
'AMD',
'BAC' ,
'AMZN',
'GE',
'AAL',
'NIO',
'BABA',
'DIS',
'NFLX',
'F',
'NVDA',
'SNAP',
'T',
'UBER',
'ROKU',
'MU',
'SPCE',
'JPM',
'TWTR',
'WFC',
'DAL',
'BYND',
'INTC',
'SQ',
'CCL',
'GILD',
'XOM',
'C',
'UAL',
'ZM',
'WMT',
'PFE',
'NKLA',
'TLRY',
'MGM',
'CSCO',
'LK',
'OXY',
'M',
'DIA',
'WORK',
'SBUX',
'JD',
'FCX',
'X',
'ET',
'PBR',
'HTZ',
'V',
'PTON',
'QCOM',
'INO',
'NCLH',
'CGC',
'KRE',
'MRNA',
'TEVA',
'PCG',
'RCL',
'GM',
'PYPL',
'LYFT',
'SHOP',
'KO',
'WYNN',
'DKNG',
'GOLD',
'BMY',
'PINS',
'VZ',
'GOOGL',
'ACB',
'NOK',
'CRM',
'LUV',
'HAL',
'TGT',
'MS',
'BBBY',
'VALE',
'AMRN',
'BIDU',
'SMH',
'SDC',
'JNJ',
'ABBV',
'GS',
'HD',
'COST',
'CVS',
'CMCSA',
'NKE',
'LVS',
'PLUG',
'CRON',
'ORCL',
'MA',
'CVX',
'BP',
'ATVI',
'EBAY',
'VIAC',
'SLB',
'MCD',
'CAT',
'BRKB',
'CRWD',
'PENN',
'ZNGA',
'LULU',
'TWLO',
'CLF',
'RIG',
'AMAT',
'MRK',
'APA',
'FDX',
'FEYE',
'TSM',
'MRVL',
'AUY',
'KHC',
'S',
'MRO',
'EXPE',
'UNH',
'MPC',
'NEM',
'ADBE',
'UPS',
'PDD',
'GME',
'ABT',
'AMC',
'CZR',
'WDC',
'DOCU',
'IQ',
'MO',
'OPK',
'AXP',
'CHWY',
'LB',
'MMM',
'KR',
'PG',
'WKHS',
'AZN',
'GSX',
'SRNE',
'GPS',
'SPOT',
'W'
]
    for si in symbols:
        es = get_yahoo_earnings(si)
        if len(es) > 0:
            df = pd.DataFrame(data=es)
            sname = epath + os.sep + si + '.csv'
            print('保存', sname)
            df.to_csv(sname, index=False)
        else:
            print('无{}数据!'.format(si))