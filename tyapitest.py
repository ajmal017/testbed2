from myibapi import *

vxx = make_contract('VXX', 303019419, exchange='SMART')
uvxy = make_contract('UVXY', 331641621, exchange='SMART')
vixy = make_contract('VIXY', 280905856, exchange='SMART')
clist = [vxx]
filepath = r'E:\ibdata'
app = myClient(clist, filepath)
app.connect('127.0.0.1', 4002, 0)
app.run()