import sys
sys.path.append("..")
from myfuncs import cumcovert
import pandas as pd
from random import randint
import copy
import os

def stockstats(symbol, win=30):
    path = 'E:\stockdata'
    stock = pd.read_csv(path + os.sep + symbol + '.csv')
    # stock = stock[: 10255]
    c = list(stock['Close'])
    h = list(stock['High'])
    l = list(stock['Low'])

    adjclistCom = []
    adjclistMin = []
    adjclistMax = []
    adjclistMinC = []
    adjclistMaxC = []
    for i in range(len(c)):
        if i + win <= len(c):
            subclistl = l[i: i + win]
            mincl = min(subclistl)
            adjcMin = (mincl - c[i]) / c[i]
            adjclistMin.append(adjcMin)

            subclisth = h[i: i + win]
            maxch = max(subclisth)
            adjcMax = (maxch - c[i]) / c[i]
            adjclistMax.append(adjcMax)

            subclistlc = c[i: i + win]
            minclc = min(subclistlc)
            adjcMinlc = (minclc - c[i]) / c[i]
            adjclistMinC.append(adjcMinlc)

            subclisthc = c[i: i + win]
            maxchc = max(subclisthc)
            adjcMaxhc = (maxchc - c[i]) / c[i]
            adjclistMaxC.append(adjcMaxhc)

            adjc = (c[i + win - 1] - c[i]) / c[i]
            adjclistCom.append(adjc)
    datadict = {}
    hist, bins = cumcovert(adjclistCom)
    datadict['Com'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMax)
    datadict['Max'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMin)
    datadict['Min'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMaxC)
    datadict['Max-C'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMinC)
    datadict['Min-C'] = (copy.deepcopy(hist), copy.deepcopy(bins))

    return datadict


def stockstats_sample(symbol, win=30, samplerio=0.1):
    path = 'E:\stockdata'
    stock = pd.read_csv(path + os.sep + symbol + '.csv')
    c = list(stock['Close'])
    h = list(stock['High'])
    l = list(stock['Low'])

    sampleNums = []
    samplelen = int(len(c) * samplerio)
    for si in range(samplelen):
        sampleNums.append(randint(0, len(c)))

    adjclistCom = []
    adjclistMin = []
    adjclistMax = []
    adjclistMinC = []
    adjclistMaxC = []
    for i in sampleNums:
        if i + win <= len(c):
            subclistl = l[i: i + win]
            mincl = min(subclistl)
            adjcMin = (mincl - c[i]) / c[i]
            adjclistMin.append(adjcMin)

            subclisth = h[i: i + win]
            maxch = max(subclisth)
            adjcMax = (maxch - c[i]) / c[i]
            adjclistMax.append(adjcMax)

            subclistlc = c[i: i + win]
            minclc = min(subclistlc)
            adjcMinlc = (minclc - c[i]) / c[i]
            adjclistMinC.append(adjcMinlc)

            subclisthc = c[i: i + win]
            maxchc = max(subclisthc)
            adjcMaxhc = (maxchc - c[i]) / c[i]
            adjclistMaxC.append(adjcMaxhc)

            adjc = (c[i + win - 1] - c[i]) / c[i]
            adjclistCom.append(adjc)
    datadict = {}
    clen = len(adjclistCom)
    if clen > 500:
        clen = 500
    hist, bins = cumcovert(adjclistCom, clen)
    datadict['Com'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMax, clen)
    datadict['Max'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMin, clen)
    datadict['Min'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMaxC, clen)
    datadict['Max-C'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMinC, clen)
    datadict['Min-C'] = (copy.deepcopy(hist), copy.deepcopy(bins))

    return datadict


def stockstats_subsp(stock, win=30):
    c = list(stock['Close'])
    h = list(stock['High'])
    l = list(stock['Low'])

    adjclistCom = []
    adjclistMin = []
    adjclistMax = []
    adjclistMinC = []
    adjclistMaxC = []
    for i in range(len(c)):
        if i + win <= len(c):
            subclistl = l[i: i + win]
            mincl = min(subclistl)
            adjcMin = (mincl - c[i]) / c[i]
            adjclistMin.append(adjcMin)

            subclisth = h[i: i + win]
            maxch = max(subclisth)
            adjcMax = (maxch - c[i]) / c[i]
            adjclistMax.append(adjcMax)

            subclistlc = c[i: i + win]
            minclc = min(subclistlc)
            adjcMinlc = (minclc - c[i]) / c[i]
            adjclistMinC.append(adjcMinlc)

            subclisthc = c[i: i + win]
            maxchc = max(subclisthc)
            adjcMaxhc = (maxchc - c[i]) / c[i]
            adjclistMaxC.append(adjcMaxhc)

            adjc = (c[i + win - 1] - c[i]) / c[i]
            adjclistCom.append(adjc)
    datadict = {}
    hist, bins = cumcovert(adjclistCom)
    datadict['Com'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMax)
    datadict['Max'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMin)
    datadict['Min'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMaxC)
    datadict['Max-C'] = (copy.deepcopy(hist), copy.deepcopy(bins))
    hist, bins = cumcovert(adjclistMinC)
    datadict['Min-C'] = (copy.deepcopy(hist), copy.deepcopy(bins))

    return datadict

def stockstats_sublist(symbol, win=30, sublist=[0.7]):
    path = 'E:\stockdata'
    stock = pd.read_csv(path + os.sep + symbol + '.csv')
    slen = len(stock)
    substocks = {}
    sNums = []
    for sui in range(len(sublist)):
        if sui == 0:
            ul = int(slen * sublist[0])
            Num = (0, ul)
            sNums.append(Num)
        else:
            dl = int(slen * sublist[sui - 1])
            ul = int(slen * sublist[sui])
            Num = (dl, ul)
            sNums.append(Num)
        if sui == len(sublist) - 1:
            dl = int(slen * sublist[sui])
            Num = (dl, slen)
            sNums.append(Num)

    for ni in sNums:
        subdata = stock[ni[0]: ni[1]]
        substocks[ni] = copy.deepcopy(subdata)

    returndatadict = {}
    for ssk, ssv in substocks.items():
        datadict = stockstats_subsp(ssv, win)
        returndatadict[ssk] = copy.deepcopy(datadict)

    return returndatadict

