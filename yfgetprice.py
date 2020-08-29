from iexfinance.stocks import Stock
import pandas as pd
import os

path = r'E:\newdata\OCC data\Adj Data'
filename = '202006-Mergers.csv'
savename1 = '202006-Mergers-Adj-NonDrop.csv'
savename2 = '202006-Mergers-Adj.csv'

data = pd.read_csv(path + os.sep + filename)
symbols = list(data['Underlying Security'])
prices = [0] * len(symbols)

pricelimit = 50
dropidxes = []
n = 0
for i in symbols:
    s = i.strip()
    print(n, s)
    try:
        ticker = Stock(s)
        qt = ticker.get_quote()
        price = float(qt['iexRealtimePrice'])
        prices[n] = price
        print(s, price)
    except:
        print(s, '获取价格失败！')
    n += 1
    print()


data['Underlying Price'] = prices
data.to_csv(path + os.sep + savename1, index=False)

# dropidxes = [ni for ni in range(len(prices)) if prices[ni] < pricelimit]
# data = data.drop(dropidxes)
# data = data.reset_index(drop=True)
#
# data.to_csv(path + os.sep + savename2, index=False)


