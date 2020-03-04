import yfinance as yf
import os

filepath = r'E:\stockdata'
symbol = 'VIIX'

tikcker = yf.Ticker(symbol)
hist = tikcker.history(period='max')
hist.to_csv(filepath + os.sep + symbol + '.csv')
print(symbol, ' done!')
