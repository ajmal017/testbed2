import pandas as pd
from copy import deepcopy
import sys
import os


UnderlyingsPath = r'D:\IB Data\Underlying'
AdjUnderlyingfile = r'D:\IB Data\Adj Underlying\adjunderlyings.csv'


def mixedType_to_float(x):
    rec = ('C', 'c', ',')
    y = x
    if isinstance(y, str):
        for ri in rec:
            if ri in y:
                y = y.replace(ri, '')
    return float(y)


def isfloat(x):
    gbs = ['inf', 'infinity', 'INF', 'INFINITY', 'True', 'NAN', 'nan', 'False', '-inf', '-INF', '-INFINITY',
           '-infinity', 'NaN', 'Nan']
    rec = ('C', 'c', ',')
    y = x
    if isinstance(y, str):
        for ri in rec:
            if ri in y:
                y = y.replace(ri, '')
    try:
        float(y)
        if str(y) in gbs:
            return False
        else:
            return True
    except:
        return False


def ispercentage(x):
    if isinstance(x, str):
        if '%' not in x:
            return False
        else:
            return True
    else:
        return False


def pick_same_nums(x: list):
    pickednums = []
    for i in range(len(x)):
        if i > 0:
            if x[i] == x[i - 1]:
                pickednums.append(i)
    return pickednums


def Pick_Underlyings_base_Change_Percentage(picknum=100, greatAbsChg=0.02, greatVOL=100000):
    files = os.listdir(UnderlyingsPath)
    underlyingdf = ''
    init = False
    for fi in files:
        df = pd.read_csv(UnderlyingsPath + os.sep + fi, encoding='gb18030', thousands=',')
        if not init:
            underlyingdf = df
            init = True
        else:
            underlyingdf = underlyingdf.append(df, ignore_index=True)

    underlyingdf = underlyingdf.reset_index(drop=True)
    underlyingdf = underlyingdf.loc[:, ~underlyingdf.columns.str.contains('Unnamed')]

    Chg = list(underlyingdf['变化%'])
    last = list(underlyingdf['最后价'])
    avgVol = list(underlyingdf['平均交易量'])

    delnums = []
    for li in range(len(last)):
        if not isfloat(last[li]):
            delnums.append(li)
    for ai in range(len(avgVol)):
        if not isfloat(avgVol[ai]):
            delnums.append(ai)
    for Ii in range(len(Chg)):
        if not ispercentage(Chg[Ii]):
            delnums.append(Ii)

    delnums = list(set(delnums))
    underlyingdf = underlyingdf.drop(index=delnums).reset_index(drop=True)
    Chg = list(underlyingdf['期权隐含波动率%'].str.strip('%').astype(float) / 100)
    AbsChg = [abs(mixedType_to_float(i)) for i in Chg]

    underlyingdf['绝对变化'] = AbsChg

    underlyingdf['最后价'] = [mixedType_to_float(i) for i in underlyingdf['最后价']]
    underlyingdf['平均交易量'] = [int(mixedType_to_float(i)) for i in underlyingdf['平均交易量']]
    underlyingdf.sort_values('金融产品', ascending=False, inplace=True)
    underlyingdf = underlyingdf.reset_index(drop=True)

    symbols = list(underlyingdf['金融产品'])
    delnums2 = pick_same_nums(symbols)
    underlyingdf = underlyingdf.drop(index=delnums2).reset_index(drop=True)
    underlyingdf.sort_values('期权隐含波动率', ascending=False, inplace=True)
    underlyingdf = underlyingdf.reset_index(drop=True)

    AbsChg = underlyingdf['绝对变化']
    if AbsChg[-1] > greatAbsChg:
        pass
    elif AbsChg[0] < greatAbsChg:
        input('无IV大于{}的标的！'.format(greatAbsChg))
        print('程序退出！')
        sys.exit(2)
    else:
        for ii in range(len(AbsChg)):
            if AbsChg[ii] < greatAbsChg:
                underlyingdf = underlyingdf[: ii]
                break

    buffdf = deepcopy(underlyingdf)
    buffdf.sort_values('平均交易量', ascending=False, inplace=True)
    buffdf = buffdf.reset_index(drop=True)
    underlyingdf = deepcopy(buffdf)
    avgVol = list(underlyingdf['平均交易量'])
    if avgVol[-1] > greatVOL:
        pass
    elif avgVol[0] < greatVOL:
        input('无avgVOL大于{}的标的！'.format(greatVOL))
        print('程序退出！')
        sys.exit(3)
    else:
        for ai in range(len(avgVol)):
            if avgVol[ai] < greatVOL:
                underlyingdf = underlyingdf[: ai]
                break

    underlyingdf.sort_values('绝对变化', ascending=False, inplace=True)
    underlyingdf = underlyingdf.reset_index(drop=True)
    if len(underlyingdf) > picknum:
        underlyingdf = underlyingdf.head(picknum)

    underlyingdf.to_csv(AdjUnderlyingfile, index=False)

    print('挑选标的完成，共选中{}个标的！'.format(len(underlyingdf)))
    return underlyingdf
