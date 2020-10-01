from IB_Utils_8 import myClient_get_STK_Tickdata_2, make_contract

conlist = []
eur = make_contract(symbol='EUR', conID=12087792, currency='USD', secType='CASH', exchange='IDEALPRO')
conlist.append(eur)

app = myClient_get_STK_Tickdata_2(conlist)
app.connect('127.0.0.1', 4003, 1)
app.run()