import urllib.request as request
import os

path = r'E:\newdata\OCC data'
months = ['201808', '201809', '201810', '201811', '201812', '201901', '201902', '201903', '201904', '201905', '201906',
          '201907', '201908', '201909', '201910', '201911', '201912', '202001', '202002', '202003', '202004', '202005',
          '202006', '202007', '202008']
premonth = ['201807']
day = '01'
exchanges = ['amex', 'arca', 'bats', 'box', 'c2', 'cboe', 'cfe', 'edgx', 'emld', 'gem', 'ise', 'mcry', 'miax', 'mprl',
             'nfx', 'nobo', 'nsdq', 'one', 'phlx']
url1 = 'https://marketdata.theocc.com/volbyclass-reports?reportDate='
url2 = '&reportClass='
url3 = '&format=csv'

monthnames = premonth + months
mn = 0
for mi in months:
    monthname = path + os.sep + monthnames[mn]
    if not os.path.exists(monthname):
        os.mkdir(monthname)
    for ei in exchanges:
        url = url1 + mi + day + url2 + ei + url3
        savename = monthname + os.sep + 'OptVol-' + monthnames[mn] + '-' + ei + '.csv'
        if not os.path.exists(savename):
            try:
                req = request.Request(url)
                res = request.urlopen(req)
                file = res.read()
                f = open(savename, 'wb')
                f.write(file)
                f.close()
                print(savename, '下载成功！')
            except:
                print(savename, '下载失败！')
    mn += 1
print('-------所有数据下载完成！--------')
