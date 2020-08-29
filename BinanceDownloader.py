from binance.client import Client

apikey = 'CY1OvqHz8SRh6hwLn9GoLSvAkrxBKWldAQtrS5Dq7OFgoErdWSL9M8l7Q29cs1Lh'
secretkey = 'sIirO27ZK2IDkZoDu2orhUntMxvL1Gy4BxPG4amMwoFevi9d8oTv627JhH2jHHmB'
wpath = r'E:\newdata\Binance Data'

myclient = Client(api_key=apikey, api_secret=secretkey)
t = myclient.get_all_tickers()
print(t)