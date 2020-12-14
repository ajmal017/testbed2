import pandas as pd
from yfinance import utils
import time

_url = 'https://finance.yahoo.com/quote'


def get_FUT_quotes(symbol: str):
    url = "{}/{}/holders".format(_url, symbol)
    dfs = pd.read_html(url)
    bid = float(dfs[0][1][3])
    ask = float(dfs[1][1][3])
    return bid, ask


def get_FUT_chain(symbol: str):
    url = '{}/{}'.format(_url, symbol)
    fc = utils.get_json(url)['futuresChain']['futures']
    return fc


if __name__ == '__main__':
    while True:
        bid, ask = get_FUT_quotes('ES=F')
        print('Bid:{} Ask:{}'.format(bid, ask))
        time.sleep(1)
