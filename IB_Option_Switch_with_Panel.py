from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QWidget, QApplication
from Form_Switch import Form_switch
import urllib.request as request
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from IB_Utils import IBdate_to_Date, Date_to_IBdate
from iexfinance.stocks import Stock
import pandas as pd
import functools
import math
import copy
import os
import sys

# occdatapath = r'E:\newdata\OCC data'
# exchanges = ['amex', 'arca', 'bats', 'box', 'c2', 'cboe', 'cfe', 'edgx', 'emld', 'gem', 'ise', 'mcry', 'miax', 'mprl',
#              'nfx', 'nobo', 'nsdq', 'one', 'phlx']
# url1 = 'https://marketdata.theocc.com/volbyclass-reports?reportDate='
# url2 = '&reportClass='
# url3 = '&format=csv'


def OccMonth_to_Date(month: str):
    year = int(month[:4])
    month = int(month[4:])
    return date(year, month, 1)


def update_OCC_data():
    occdatapath = r'E:\newdata\OCC data'
    exchanges = ['amex', 'arca', 'bats', 'box', 'c2', 'cboe', 'cfe', 'edgx', 'emld', 'gem', 'ise', 'mcry', 'miax',
                 'mprl',
                 'nfx', 'nobo', 'nsdq', 'one', 'phlx']
    url1 = 'https://marketdata.theocc.com/volbyclass-reports?reportDate='
    url2 = '&reportClass='
    url3 = '&format=csv'

    monthlist = os.listdir(occdatapath)
    aidx = monthlist.index('Adj Data')
    monthlist.pop(aidx)
    monthlist = list(sorted(monthlist))
    leatestdate = OccMonth_to_Date(monthlist[-1])
    m1day = date(date.today().year, date.today().month, 1)
    leatestdate = leatestdate + relativedelta(months=1)
    downloadmonths = []
    while leatestdate < m1day:
        downloadmonths.append(copy.deepcopy(leatestdate))
        leatestdate = leatestdate + relativedelta(months=1)

    if len(downloadmonths) != 0:
        mpaths = []
        for mi in downloadmonths:
            m0 = Date_to_IBdate(mi)[:6]
            m1 = Date_to_IBdate(mi + relativedelta(months=1))
            mpath = occdatapath + os.sep + m0
            mpaths.append(mpath)
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            for ei in exchanges:
                url = url1 + m1 + url2 + ei + url3
                savename = mpath + os.sep + 'OptVol-' + m0 + '-' + ei + '.csv'
                try:
                    req = request.Request(url)
                    res = request.urlopen(req)
                    file = res.read()
                    # print(len(file))
                    if len(file) != 0:
                        f = open(savename, 'wb')
                        f.write(file)
                        f.close()
                        print(savename, '下载成功！')
                    else:
                        print('无数据！')
                except:
                    print(savename, '下载失败！')
        for ri in mpaths:
            rl = os.listdir(ri)
            if len(rl) == 0:
                os.rmdir(ri)
        print('OCC 文件下载完成！')
    else:
        print('文件为最新状态，无需更新！')


class update_occ_data_thread(QThread):
    def __init__(self):
        QThread.__init__(self)

    def run(self):
        update_OCC_data()


def pick_underlyings(aboveprice=50):
    occdatapath = r'E:\newdata\OCC data'
    savepath = r'E:\newdata\OCC data\Adj Data'
    monthlist = os.listdir(occdatapath)
    aidx = monthlist.index('Adj Data')
    monthlist.pop(aidx)
    monthlist = list(sorted(monthlist))
    leatestmonth = monthlist[-1]
    workpath = occdatapath + os.sep + leatestmonth

    fileslist = os.listdir(workpath)
    fdata = ''
    finit = False
    for fi in fileslist:
        ff = workpath + os.sep + fi
        if os.stat(ff).st_size != 0:
            fdf = pd.read_csv(ff, thousands=',')
            fdf = fdf[: -2]
            if not finit:
                fdata = fdf
                finit = True
                continue
            fnames = list(fdata['Options Class'])
            dfnames = list(fdf['Options Class'])
            for ui in range(len(dfnames)):
                if dfnames[ui] in fnames:
                    idx = fnames.index(dfnames[ui])
                    fdata.at[idx, 'Trade Volume'] += fdf.at[ui, 'Trade Volume']
                    fdata.at[idx, 'YTD Volume'] += fdf.at[ui, 'YTD Volume']
                else:
                    ps = fdf.iloc[ui]
                    fdata = fdata.append(ps, ignore_index=True)

    fdata.sort_values('YTD Volume', ascending=False, inplace=True)
    savename = leatestmonth + '-Full.csv'
    fdata.to_csv(savepath + os.sep + savename, index=False)

    symbols = list(fdata['Underlying Security'])
    col = fdata.columns
    pickedDf = pd.DataFrame(columns=col)
    # pickinit = False
    prices = []
    n = 0
    sn = 0
    while n < 200:
        for si in symbols:
            sy = si.strip()
            try:
                ticker = Stock(sy)
                qt = ticker.get_quote()
                price = float(qt['iexRealtimePrice'])
                if price > aboveprice:
                    prices.append(price)
                    ps = fdata.iloc[sn]
                    pickedDf.append(ps, ignore_index=True)
                    print('获取到第{}支股票{}的价格为{}'.format(n, sy, price))
                    n += 1
            except:
                print('获取{}价格失败！'.format(sy))
            sn += 1
    pickedDf['Price'] = prices
    pickedDf.to_csv()





class IB_Option_Switch_with_Panel(Form_switch):
    def __init__(self):
        Form_switch.__init__(self)
        self.OCC_thread = update_occ_data_thread()

    @pyqtSlot()
    def slot_update_OCC_data(self):
        self.OCC_thread.start()

    @pyqtSlot()
    def slot_pick_underlyings(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    form = IB_Option_Switch_with_Panel()
    form.show()

    sys.exit(app.exec_())