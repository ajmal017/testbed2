import pandas as pd
import os

symbol = 'EURUSD'
pricestype = 'midpoint'
unPackpath = r'D:\TrueFX Data\Pairs Sub Data\{}'.format(symbol)
mergepath = r'D:\TrueFX Data\Merged Data\{}-{}.txt'.format(symbol, pricestype)

files = os.listdir(unPackpath)
files = list(sorted(files))
for i in files:
    print('读取', i)
    df = pd.read_csv(unPackpath + os.sep + i, header=None)
    midpoint = round((df[2] + df[3]) / 2, 5)
    midpoint.to_csv(mergepath, index=False, header=None, mode='a+')
print(symbol, '数据处理完成！')