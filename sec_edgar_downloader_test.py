from sec_edgar_downloader import Downloader

path = 'E:\stockdata3\Filings'
dl = Downloader(path)
aapl = dl.get('10-K', 'aapl', 30)
pass