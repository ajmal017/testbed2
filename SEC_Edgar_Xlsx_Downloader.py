from sec_edgar_downloader._utils import get_filing_urls_to_download as get_urls
from datetime import date
import urllib.request as request
import pandas as pd
import os

path = 'E:\stockdata3'
tickers = list(pd.read_csv(path + os.sep + 'CIKs.csv')['Ticker'])
CIKs = list(pd.read_csv(path + os.sep + 'CIKs.csv')['CIK'])
flen = len(CIKs)

n = 0
downloadbreakpointfile = path + os.sep + 'DownloadBreakPoint.txt'
if os.path.exists(downloadbreakpointfile):
    tf = open(downloadbreakpointfile, 'r')
    downloadbp = tf.read()
    tf.close()
    startnum = tickers.index(downloadbp)
    tickers = tickers[startnum:]
    CIKs = CIKs[startnum:]
    n = startnum

CIKdict = {}
for i in range(len(tickers)):
    CIKdict[tickers[i]] = CIKs[i]

filing_type = '10-K'
ticker_or_cik = ''
num_filings_to_download = 11
after_date = None
before_date = date.today().strftime("%Y%m%d")

fpath = path + os.sep + 'XlsxFilings'
if not os.path.exists(fpath):
    os.mkdir(fpath)

pre_url = 'https://www.sec.gov/Archives/edgar/data/'
post_urlx = '/Financial_Report.xlsx'
post_url = '/Financial_Report.xls'

for ti in tickers:
    f = open(downloadbreakpointfile, 'w')
    f.write(ti)
    f.close()

    print('---------', ti, '----------')

    filings = get_urls(filing_type, ti, num_filings_to_download, after_date, before_date, False)

    typepath = fpath + os.sep + ti + os.sep + filing_type
    if not os.path.exists(typepath):
        os.makedirs(typepath)
    cik = CIKdict[ti]

    xsslt = True
    for fi in filings:
        filename = fi.filename
        filenamesv = filename.split('.')[0]

        existedfiles = list(os.listdir(typepath))
        adjexistedfiles = [i.split('.')[0] for i in existedfiles]

        if filenamesv not in adjexistedfiles:
            filenamesplit = filenamesv.split('-')
            filenameurl = filenamesplit[0] + filenamesplit[1] + filenamesplit[2]

            def try2():
                savename = filenamesv + '.xls'
                url = pre_url + str(cik) + '/' + filenameurl + '/' + post_url
                savepath = typepath + os.sep + savename
                try:
                    req = request.Request(url)
                    res = request.urlopen(req)
                    file = res.read()
                    f = open(savepath, 'wb')
                    f.write(file)
                    f.close()
                    print(savename, '下载完成！')
                    return False
                except:
                    print(savename, '下载失败！')
                    return True

            if xsslt:
                savenamex = filenamesv + '.xlsx'
                urlx = pre_url + str(cik) + '/' + filenameurl + '/' + post_urlx
                savepathx = typepath + os.sep + savenamex
                try:
                    req = request.Request(urlx)
                    res = request.urlopen(req)
                    file = res.read()
                    f = open(savepathx, 'wb')
                    f.write(file)
                    f.close()
                    print(savenamex, '下载完成！')
                except:
                    xsslt = False
                    t = try2()
                    if t:
                        break
                    continue
            else:
                bt = try2()
                if bt:
                    break

    n += 1
    drio = round(n * 100 / flen, 2)
    print('-------',  ti, '下载完成！ 总进度：' + str(drio) + '% --------')