from urllib import request
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import os

hpath = r'E:\HTML'
hf = 't1'
hfp = hpath + os.sep + hf + '.html'
url = 'https://finance.yahoo.com/calendar/earnings?from=2020-12-13&to=2020-12-19&day=2020-12-19'

proxy_addr = {'https': 'http://127.0.0.1:10809', 'http': 'http://127.0.0.1:10809'}
proxy = request.ProxyHandler(proxy_addr)
opener = request.build_opener(proxy, request.HTTPHandler)
request.install_opener(opener)
html = request.urlopen(url)

# f = open(hfp, 'r', encoding='UTF-8')
htmldoc = html.read().decode('utf-8')
# print(htmldoc)
soup = bs(htmldoc, features='lxml')
earnings = {}

# tds = soup.find_all('td', {'class': "line-content"})
# txt = tds[51].text
# print(txt)
#
# if txt.startswith('root.App.main = '):
#     jh, _, jdata = txt.partition('=')
#     jdata = jdata[0: -1]
#     jdict = json.loads(jdata)
#     earnings = jdict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
#
# else:
#     for ti in tds:
#         txt = ti.text
#         if txt.startswith('root.App.main = '):
#             jh, _, jdata = txt.partition('=')
#             jdata = jdata[0: -1]
#             jdict = json.loads(jdata)
#             earnings = jdict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']

spts = soup.find_all('script')

n = 0
jtxt = ''
for si in spts:
    txt = si.string
    if txt:
        if txt.startswith('\n(function (root)'):
            print(txt)
            n += 1
            jtxt = txt
            break

jh, _, jdata = jtxt.partition('root.App.main = ')
jdata = jdata[0: -12]
jdict = json.loads(jdata)
earnings = jdict['context']['dispatcher']['stores']['ScreenerResultsStore']['results']['rows']
pass