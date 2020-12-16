import pandas as pd
import math
import os


def keep_float_digit(f: float, d: int):
    fi = int(f * pow(10, d))
    return fi / pow(10, d)


mergepath = r'D:\TrueFX Data\Merged Data'
brickpath = r'D:\TrueFX Data\Bricks Data'
pairs = 'EURUSD'
filename = mergepath + os.sep + pairs + '.csv'
df = pd.read_csv(filename, header=None)
print('DF读取完成！')
dl = len(df)
bpnum = 10
gap = 0.0001 * bpnum
brickfile = brickpath + os.sep + pairs + '-bricks-{}bp.txt'.format(bpnum)


def write_brick_data(data: str):
    f = open(brickfile, 'a+')
    f.write(data)
    f.close()


lastforth = True
currentforth = True
baropen = 0
barclose = 0
baropentime = ''
barclosetime = ''
bargapnum = 0
barstdcloseP = 0
barstdcloseN = 0
opennextbar = False

sdata = []
for i in range(dl):
    if i == 0:
        baropen = df[2][0]
        barstdcloseP = keep_float_digit(baropen + gap, 4)
        barstdcloseN = keep_float_digit(baropen - 2 * gap, 4)
        baropentime = df[0][0]
    else:
        if currentforth:
            eprice = df[1][i]

            if opennextbar:
                if lastforth == currentforth:
                    baropen = eprice
                else:
                    baropen = df[2][i]

                baropentime = df[0][i]
                opennextbar = False

            if eprice >= barstdcloseP:
                bargapnum = 1
                while barstdcloseP + bargapnum * gap <= eprice:
                    bargapnum += 1
                    print(1, bargapnum)
                barclose = eprice
                barclosetime = df[0][i]
                sdata = [baropentime, barclosetime, str(baropen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                opennextbar = True
                lastforth = currentforth

                barstdcloseP += (gap * bargapnum)
                barstdcloseN += (gap * bargapnum)

            elif eprice <= barstdcloseN:
                bargapnum = -1
                while barstdcloseN + bargapnum * gap >= eprice:
                    bargapnum -= 1
                    print(2, bargapnum)
                barclose = eprice
                barclosetime = df[0][i]
                sdata = [baropentime, barclosetime, str(baropen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                opennextbar = True

                barstdcloseP += (gap * bargapnum)
                barstdcloseN += (gap * bargapnum)
                lastforth = currentforth
                currentforth = False

        else:
            eprice = df[2][i]

            if opennextbar:
                if lastforth == currentforth:
                    baropen = eprice
                else:
                    baropen = df[1][i]

                baropentime = df[0][i]
                opennextbar = False

            if eprice <= barstdcloseN:
                bargapnum = -1
                while barstdcloseN + bargapnum * gap >= eprice:
                    bargapnum -= 1
                    print(3, bargapnum)
                barclose = eprice
                barclosetime = df[0][i]
                sdata = [baropentime, barclosetime, str(baropen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                opennextbar = True
                lastforth = currentforth

                barstdcloseP += (gap * bargapnum)
                barstdcloseN += (gap * bargapnum)

            elif eprice >= barstdcloseP:
                bargapnum = 1
                while barstdcloseP + bargapnum * gap <= eprice:
                    bargapnum += 1
                    print(4, bargapnum)
                barclose = eprice
                barclosetime = df[0][i]
                sdata = [baropentime, barclosetime, str(baropen), str(barclose), str(bargapnum)]
                write_brick_data(','.join(sdata) + '\n')
                opennextbar = True

                barstdcloseP += (gap * bargapnum)
                barstdcloseN += (gap * bargapnum)
                lastforth = currentforth
                currentforth = True

    rm = round(i / (dl - 1) * 100, 2)
    print(i, '完成{}%'.format(rm))