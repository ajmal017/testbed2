# import pandas as pd
# import os
# from collections import Counter
#
# # path = 'E:\\newdata\CN Oils'
# # n1 = '伦敦布伦特原油期货历史数据'
# # n2 = '伦敦布伦特原油期货历史数据 (1)'
# # d1 = pd.read_csv(path + os.sep + n1 + '.csv')
# # d2 = pd.read_csv(path + os.sep + n2 + '.csv')
# #
# # dl = [d1, d2]
# # dll = pd.concat(dl)
# #
# # dll.to_csv(path + os.sep + 'Brent.csv')
#
#
# l = [1,2,3,5,2,4,2,41,6,]
# t = Counter(l)
# pass

from Quandl_Utils import Quandl_Treasury_Constant_Maturity_Rate_Downloader

Quandl_Treasury_Constant_Maturity_Rate_Downloader()