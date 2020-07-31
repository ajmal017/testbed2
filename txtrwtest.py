import os


path = 'E:\stockdata3'

tf = open(path + os.sep + 'DownloadBreakPoint.txt', 'r')
txt = tf.read()
tf.close()
pass