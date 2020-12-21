import pandas as pd
import os
from datetime import datetime

starttime = datetime.now()


def keep_float_digit(f: float, d: int):
    fi = int(f * pow(10, d))
    return fi / pow(10, d)


mergepath = r'D:\TrueFX Data\Merged Data'
brickpath = r'D:\TrueFX Data\Bricks Data'
pairs = 'EURUSD'
filename = mergepath + os.sep + pairs + '-midpoint.txt'
df = pd.read_csv(filename, header=None)
print('DF读取完成！')
midpoint = df[0].values
dl = len(midpoint)
bpnum = 10
gap = 0.0001 * bpnum
brickfile = brickpath + os.sep + pairs + '-bricks-{}bp.txt'.format(bpnum)


def write_brick_data(data: str):
    f = open(brickfile, 'a+')
    f.write(data)
    f.close()


lastforth = None
currentforth = None
baropen = 0
barclose = 0
rstdopen = 0
stdopen = 0
bargapnum = 0
barstdcloseP = 0
barstdcloseN = 0

sdata = []

for i in range(dl):
    if i == 0:
        baropen = midpoint[i]
        bll = int(baropen / gap) * gap
        blh = bll + gap
        llgap = baropen - bll
        lhgap = blh - baropen
        if lhgap >= llgap:
            stdopen = bll
            barstdcloseP = stdopen + gap
            barstdcloseN = stdopen - 2 * gap
            rstdopen = stdopen - gap
            currentforth = True
        else:
            stdopen = blh
            barstdcloseP = stdopen + 2 * gap
            barstdcloseN = stdopen - gap
            rstdopen = stdopen + gap
            currentforth = False

    else:
        eprice = midpoint[i]

        if currentforth:
            if eprice >= barstdcloseP:
                bargapnum = 1
                while barstdcloseP + bargapnum * gap <= eprice:
                    bargapnum += 1
                    print(1, bargapnum)
                barclose = barstdcloseP

                sdata = [str(baropen), str(rstdopen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                lastforth = currentforth

                baropen = eprice
                stdopen += (gap * bargapnum)
                barstdcloseP = stdopen + gap
                barstdcloseN = stdopen - 2 * gap
                rstdopen = stdopen - gap

            elif eprice <= barstdcloseN:
                bargapnum = -1
                while barstdcloseN + bargapnum * gap >= eprice:
                    bargapnum -= 1
                    print(2, bargapnum)
                barclose = barstdcloseN

                sdata = [str(baropen), str(rstdopen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                lastforth = currentforth
                currentforth = False

                baropen = eprice
                stdopen = rstdopen
                stdopen += (gap * bargapnum)
                barstdcloseP = stdopen + 2 * gap
                barstdcloseN = stdopen - gap
                rstdopen = stdopen + gap

        else:
            if eprice <= barstdcloseN:
                bargapnum = -1
                while barstdcloseN + bargapnum * gap >= eprice:
                    bargapnum -= 1
                    print(3, bargapnum)
                barclose = barstdcloseN

                sdata = [str(baropen), str(rstdopen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                lastforth = currentforth

                baropen = eprice
                stdopen += (gap * bargapnum)
                barstdcloseP = stdopen + 2 * gap
                barstdcloseN = stdopen - gap
                rstdopen = stdopen + gap

            elif eprice >= barstdcloseP:
                bargapnum = 1
                while barstdcloseP + bargapnum * gap <= eprice:
                    bargapnum += 1
                    print(4, bargapnum)
                barclose = barstdcloseP

                sdata = [str(baropen), str(rstdopen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                lastforth = currentforth
                currentforth = True

                baropen = eprice
                stdopen = rstdopen
                stdopen += (gap * bargapnum)
                barstdcloseP = stdopen + gap
                barstdcloseN = stdopen - 2 * gap
                rstdopen = stdopen - gap

    rm = round(i / (dl - 1) * 100, 4)
    print(i, '完成{}%'.format(rm))

endtime = datetime.now()
timegap = endtime - starttime
print('共耗时{}秒'.format(timegap.seconds))
