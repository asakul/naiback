
import numpy as np

def ATR(bars, period):
    tr = np.zeros(len(bars.close))

    if len(bars.close) == 0:
        return np.array([])

    tr[0] = bars.high[0] - bars.low[0]
    for i in range(1, len(bars.close)):
        tr[i] = max(bars.high[i] - bars.low[i], abs(bars.high[i] - bars.close[i - 1]), abs(bars.low[i] - bars.close[i - 1]))

    atr = np.zeros(len(bars.close))
    if len(bars.close) <= period:
        return atr
    atr[period - 1] = sum(tr[0:period]) / period
    for i in range(period, len(bars.close)):
        atr[i] = (atr[i - 1] * (period - 1) + tr[i]) / period
    return atr
