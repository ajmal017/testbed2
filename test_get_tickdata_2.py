from IB_Utils_8 import myClient_get_STK_Tickdata_2, make_contract

conlist = []
eur = make_contract(symbol='EUR', conID=12087792, currency='USD', secType='CASH', exchange='IDEALPRO')
xau = make_contract(symbol='XAUUSD', conID=69067924, currency='USD', secType='CMDTY', exchange='SMART')
conlist.append(xau)

app = myClient_get_STK_Tickdata_2(conlist)
app.connect('127.0.0.1', 4003, 1)
app.run()