from QuandlDataCleaner_2_1 import termday_generator_NG
from datetime import date, timedelta

# filedict = {}
# n = 0
# for yi in range(y):
#     if yi > 0:
#         coors = []
#         ylist = list(range(yi))
#         ylist_r = list(reversed(ylist))
#         for ni in range(yi):
#             coor = (ylist[ni], ylist_r[ni])
#             coors.append(coor)
#         filedict[n] = coors
#         n += 1
#
# ylist_R = list(reversed(list(range(y))))
#
# for xi in range(x - y):
#     coors = []
#     xn = 0
#     for yi in ylist_R:
#         coor = (xi + xn, yi)
#         xn += 1
#         coors.append(coor)
#     filedict[n] = coors
#     n += 1
#
# ylist_e = list(range(y))
#
# for i in ylist_e:
#     ylist_e_x = list(range(x - y + i, x))
#     ylist_e_y = list(reversed(list(range(i, y))))
#     coors = []
#     for yi in range(len(ylist_e_y)):
#         coor = (ylist_e_x[yi], ylist_e_y[yi])
#         coors.append(coor)
#     filedict[n] = coors
#     n += 1


def split_coors_generator(x: int, y: int):
    filedict = {}
    n = 0
    for xi in range(x):
        if xi > 0:
            coors = []
            xlist = list(range(xi))
            xlist_r = list(reversed(xlist))
            for ni in range(xi):
                coor = (xlist_r[ni], xlist[ni])
                coors.append(coor)
            filedict[n] = coors
            n += 1

    xlist_R = list(reversed(list(range(x))))

    for yi in range(y - x):
        # if yi > 0:
        coors = []
        yn = 0
        for xi in xlist_R:
            coor = (xi, yi + yn)
            yn += 1
            coors.append(coor)
        filedict[n] = coors
        n += 1

    xlist_e = list(range(x))

    for i in xlist_e:
        # if i > 0:
        xlist_e_y = list(range(y - x + i, y))
        xlist_e_x = list(reversed(list(range(i, x))))
        coors = []
        for ii in range(len(xlist_e_x)):
            coor = (xlist_e_x[ii], xlist_e_y[ii])
            coors.append(coor)
        filedict[n] = coors
        n += 1

    return filedict


# x = 24
# y = 293
# d = split_coors_generator(x, y)
# pass
td = date(2021, 2, 2)
d = termday_generator_NG(td)
pass