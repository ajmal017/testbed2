import pandas as pd
import os

symbol = 'XAUUSD'
unPackpath = r'D:\HIST Data\unPacked\{}'.format(symbol)
mergepath = r'D:\HIST Data\Merged\{}-tick.txt'.format(symbol)

files = os.listdir(unPackpath)
files = list(sorted(files))
for i in files:
    postx = i.split('.')[-1]
    if postx == 'csv':
        print('读取', i)
        df = pd.read_csv(unPackpath + os.sep + i, header=None)
        midpoint = round((df[2] + df[1]) / 2, 3)
        midpoint.to_csv(mergepath, index=False, header=None, mode='a+')
print(symbol, '数据处理完成！')

