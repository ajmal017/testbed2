from myiboptapi2 import make_contract, myClient3

stricklist = list(range(300, 361, 1))
filepath = r'E:\ibdata3'
underlying = make_contract('VXXL', 265598, exchange='SMART')
myapp = myClient3(underlying, stricklist, filepath)
myapp.connect('127.0.0.1', 7497, 1)
myapp.run()

