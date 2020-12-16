import pandas as pd
import zipfile
import os

spath = r'C:\Users\Administrator\Downloads\Compressed'
sfiles = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September']
temppath = r'D:\TrueFX Data\Temp Data'
mergepath = r'D:\TrueFX Data\Merged Data'
subpath = r'D:\TrueFX Data\Pairs Sub Data'

procnum = 2

if procnum == 1:
    for i in sfiles:
        zfilename = spath + os.sep + i + '.zip'
        zfile = zipfile.ZipFile(zfilename)
        print('读取文件', i + '.zip')
        for zi in zfile.namelist():
            pairname = zi.split('-')[0]
            subspath = subpath + os.sep + pairname
            if not os.path.exists(subspath):
                os.mkdir(subspath)
            zifilename = temppath
            zfile.extract(zi, zifilename)
            zizfilename = zifilename + os.sep + zi
            zifile = zipfile.ZipFile(zizfilename)
            zifile.extractall(path=subspath)
            print('解压文件', zi)
            zifile.close()
            os.remove(zizfilename)
        zfile.close()

elif procnum == 2:
    symbol = 'GBPUSD'
    pairpath = subpath + os.sep + symbol
    pairnames = os.listdir(pairpath)
    pairnames = list(sorted(pairnames))

    psavename = mergepath + os.sep + symbol + '.csv'
    n = 0
    for pi in pairnames:
        print('读取', pi)
        df = pd.read_csv(pairpath + os.sep + pi, header=None)
        df.drop(axis=1, columns=0, inplace=True)
        if n == 0:
            df.to_csv(psavename, index=False, header=False)
        else:
            df.to_csv(psavename, index=False, header=False, mode='a+')
        n += 1

    print('{}合并完成！'.format(symbol))









