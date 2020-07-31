from sec_edgar_downloader._utils import get_filing_urls_to_download as get_urls
from datetime import date
import urllib.request as request
import pandas as pd
import xlrd
import os

# after_date = None
# before_date = date.today().strftime("%Y%m%d")
# urls = get_urls('10-K', 'AAPL', 11, after_date, before_date, False)
# pass

# url = 'https://www.sec.gov/Archives/edgar/data/320193/000032019319000119/Financial_Report.xlsx'
# filename = 'E:\stockdata3\\test.xlsx'
# try:
#     req = request.Request(url)
#     res = request.urlopen(req)
#     file = res.read()
#     f = open(filename, 'wb')
#     f.write(file)
#     f.close()
#     print('下载完成！')
# except:
#     print('下载失败！')

path = 'E:\stockdata3\others'
n1 = '0001193125-12-270341.xls'
n2 = '0001193125-14-237425.xlsx'
workbook = xlrd.open_workbook(path + os.sep + n2)
sheetnames = workbook.sheet_names()
sheet01 = workbook.sheet_by_index(0)
pass
