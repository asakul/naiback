
import numpy as np

from .sma import SMA

def BollingerBands(values, period, stddevs):
    lower = np.zeros(len(values))
    higher = np.zeros(len(values))
    ma = SMA(values, period)
    diffs = ma - np.array(values)
    for i in range(period, len(values)):
        #sigma = np.std(diffs[i-period+1:i+1])
        sigma = np.std(values[i-period+1:i+1])
        lower[i] = ma[i] - stddevs * sigma
        higher[i] = ma[i] + stddevs * sigma

    return (lower, higher)


