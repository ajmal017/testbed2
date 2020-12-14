from IB_Utils_10 import myClient_get_FX_Tickdata, make_contract

conlist = []
xau = make_contract(symbol='XAUUSD', conID=69067924, currency='USD', secType='CMDTY', exchange='SMART')
eur = make_contract(symbol='EUR', conID=12087792, currency='USD', secType='CASH', exchange='IDEALPRO')
conlist.append(eur)
conlist.append(xau)

app = myClient_get_FX_Tickdata(conlist)
app.connect('127.0.0.1', 4003, 1)
app.run()