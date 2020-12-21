import os


def write_data(filename:str, data: str):
    f = open(filename, 'w')
    f.write(data)
    f.close()


spath = r'D:\TradingView Data\Scripts'
color = ['aqua', 'blue', 'green', 'maroon', 'navy', 'olive', 'orange', 'purple', 'red', 'teal',
         'white', 'yellow', 'silver']
B4 = '    '


def futures_spot_spread(spot: str, fsymbol: str, months: list, ref=False):
    spotname = spot.split(':')[1]
    filename = spath + os.sep + spotname + '_F-S_spread.txt'
    studyname = spotname + '_F-S_spread_%'
    rf = ''
    if ref:
        rf = '1/'

    lines = ['\n'] * 6
    lines[0] = '//@version=4\n'
    lines[1] = 'study("{}")\n'.format(studyname)
    lines[2] = 'zero = 0\n'
    lines[3] = 'plot(zero,"Zreo Line",color.white,2)\n'
    lines[4] = 'spotclose = security("{}",timeframe.period,close)\n'.format(spot)

    n = 2
    for i in months:
        con = fsymbol + i
        ms = 'plot(100*({}security("{}",timeframe.period,close)-spotclose)/spotclose,"{}",color.{})\n'.format(rf, con, con, color[n])
        lines.append(ms)
        n += 1

    lines.append('plot(100*({}security("{}1!",timeframe.period,close)-spotclose)/spotclose,"{}1!",color.{},2,plot.style_cross,join=true)\n'.format(
        rf, fsymbol, fsymbol, color[0]))
    lines.append('plot(100*({}security("{}2!",timeframe.period,close)-spotclose)/spotclose,"{}2!",color.{},2,plot.style_circles,join=true)\n'.format(
        rf, fsymbol, fsymbol, color[1]))

    write_data(filename, ''.join(lines))


spot = 'OANDA:EURUSD'
fsymbol = '6E'
months = ['X2020', "Z2020", "F2021", "G2021", "H2021", "J2021", "M2021", "U2021", "Z2021"]
spot2 = 'OANDA:GBPUSD'
fsymbol2 = '6B'
spot3 = 'OANDA:USDJPY'
fsymbol3 = '6J'
spot4 = 'OANDA:AUDUSD'
fsymbol4 = '6A'
spot5 = 'OANDA:USDMXN'
fsymbol5 = '6M'
spot6 = 'OANDA:USDCAD'
fsymbol6 = '6C'
spot7 = 'OANDA:NZDUSD'
fsymbol7 = '6N'
months7 = ["Z2020", "H2021", "M2021", "U2021", "Z2021", 'H2022']
spot8 = 'OANDA:USDCHF'
fsymbol8 = '6S'
spot9 = 'BITBAY:BTCUSD'
fsymbol9 = 'BTC'
months9 = ['X2020', "Z2020", "F2021", "G2021", "H2021", "J2021", 'Z2021']
spot10 = 'OANDA:XAUUSD'
fsymbol10 = 'GC'
months10 = ['X2020', "Z2020", "F2021", "G2021",  "J2021", "M2021", "Q2021", "V2021", "Z2021"]
spot11 = 'OANDA:XAGUSD'
fsymbol11 = 'SI'
months11 = ["Z2020", "F2021", "H2021",  "K2021", "N2021", "U2021", "Z2021"]
futures_spot_spread(spot11, fsymbol11, months11, False)