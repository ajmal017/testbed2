import pandas as pd
import zipfile
import os

symbol = 'XAUUSD'
spath = r'D:\HIST Data\Compressed\{}'.format(symbol)
sfiles = os.listdir(spath)
unPackpath = r'D:\HIST Data\unPacked\{}'.format(symbol)
if not os.path.exists(unPackpath):
   os.mkdir(unPackpath)
mergepath = r'D:\HIST Data\Merged'

procnum = 1

if procnum == 1:
    dl = len(sfiles)
    n = 0
    for i in sfiles:
        n += 1
        zfilename = spath + os.sep + i
        zfile = zipfile.ZipFile(zfilename)
        print('读取文件', i)
        zfile.extractall(path=unPackpath)
        print(n, '解压文件', i)
        zfile.close()
        print('完成{}%'.format(round(n * 100 / dl)))
    print(symbol, '解压完成！')


elif procnum == 2:
    pairfilenames = list(sorted(os.listdir(unPackpath)))

    psavename = mergepath + os.sep + symbol + '.csv'
    n = 0
    for pi in pairfilenames:
        postx = pi.split('.')[-1]
        if postx == 'csv':
            print('读取', pi)
            df = pd.read_csv(unPackpath + os.sep + pi, header=None)
            df.drop(axis=1, columns=3, inplace=True)
            if n == 0:
                df.to_csv(psavename, index=False, header=False)
            else:
                df.to_csv(psavename, index=False, header=False, mode='a+')
            n += 1

    print('{}合并完成！'.format(symbol))