import yfinance as yf
import time
import os

filepath = r'D:\Yahoo Data\Futures'
symbol = 'BZ=F'
tikcker = yf.Ticker(symbol)
time.sleep(0.1)
hist = tikcker.history(period='max')
hist.to_csv(filepath + os.sep + symbol + '.csv')
print(symbol, ' done!')
