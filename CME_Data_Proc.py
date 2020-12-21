import os

cmepath = r'D:\CME Data'
file = 'XCME_ES_FUT_110110.TXT'
filename = cmepath + os.sep + file

condict = {}
timep = []
f = open(filename, 'r')
n = 0
while True:
    n += 1
    print('读取第{}行'.format(n))
    line = f.readline()
    if line:
        AoB = line[52]
        if AoB == 'A' or AoB == 'B':
            tsp = line[:14]
            symbol = line[23: 26] + line[27: 31]
            vol = int(line[31: 36])
            price = int(line[44: 51]) / 100

            if symbol not in condict.keys():
                condict[symbol] = []
            condict[symbol].append([tsp, AoB, price, vol])

            if tsp not in timep:
                timep.append(tsp)
    else:
        f.close()
        break
