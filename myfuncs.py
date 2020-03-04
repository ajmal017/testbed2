import pandas as pd
import numpy as np

def dataframeinsertrow(df:pd.DataFrame, n, row:list):
    columns = list(df.columns)
    insertrow = pd.DataFrame([row], columns=columns)
    if n <= 0:
        return insertrow.append(df, ignore_index=True)
    elif n >= df.__len__():
        return df.append(insertrow, ignore_index=True)
    else:
        above = df[:n]
        below = df[n:]
        newdf = pd.concat([above, insertrow, below], ignore_index=True)
        return newdf


def cumcovert(data:list, bins=200):
    hist, cbins = np.histogram(data, bins=bins, density=False)
    hist = list(hist)
    cbins = cbins[1:]
    cbins = list(cbins)
    ctotal = sum(hist)
    chist = [sum(hist[:ic + 1]) / ctotal for ic in range(len(hist))]
    return chist, cbins