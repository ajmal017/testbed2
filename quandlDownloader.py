# import urllib.request as request
# import pandas as pd
# import os
#
#
# symbolnum = 394
#
# path = r'E:\newdata\quandl data'
# url1 = 'https://www.quandl.com/api/v3/datasets/'
# url3 = '?api_key=fjZyjRt-6y5WRapHGiAY'
#
# contractfile = r'E:\newdata\quandl data\continuous.csv'
# condf = pd.read_csv(contractfile)
# code = condf['Quandl Code'][symbolnum]
# num = condf['Number of Contracts'][symbolnum]
#
# numlist = list(range(num + 1))
# numlist = numlist[1:]
#
# cs = code.split('/')
# subdir = cs[0] + '-' + cs[1]
#
# savepath = path + os.sep + subdir
# # adjpath = savepath + os.sep + 'AdjData'
# if not os.path.exists(savepath):
#     os.mkdir(savepath)
# #     os.mkdir(adjpath)
#
# for ni in numlist:
#     url2 = code + str(ni) + '.csv'
#     url = url1 + url2 + url3
#
#     us = url2.split('/')
#     filename = subdir + '-' + str(ni) + '.csv'
#
#     savename = savepath + os.sep + filename
#     filelist = os.listdir(savepath)
#     if filename not in filelist:
#         try:
#             req = request.Request(url)
#             res = request.urlopen(req)
#             file = res.read()
#             f = open(savename, 'wb')
#             f.write(file)
#             f.close()
#             print(ni, filename, '下载完成！')
#         except:
#             print(ni, filename, '下载失败！')
#
# print(subdir, '下载完成！')
#
# from Quandl_Utils import Chris_Futures_Downloader
#
# Chris_Futures_Downloader(149) #149

from Quandl_Utils import Continueous_to_Singal, SingalTermday_generator_GE
path = r'E:\newdata\quandl data\CHRIS-CME_ED'
Continueous_to_Singal(path, SingalTermday_generator_GE)