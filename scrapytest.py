import pandas as pd

url = 'https://www.tradingview.com/symbols/BTCUSD/'

data = pd.read_html(url)
pass