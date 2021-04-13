
import numpy as np

from .atr import ATR
from .ema import EMA
from .smma import SMMA

def ADX(bars, period):
    dm_minus = np.zeros(len(bars.close))
    dm_plus = np.zeros(len(bars.close))
    adx = np.zeros(len(bars.close))
    atr = ATR(bars, period)

    if len(bars.close) == 0:
        return np.array([])

    for i in range(1, len(bars.close)):
        plus = bars.high[i] - bars.high[i - 1]
        minus = -bars.low[i] + bars.low[i - 1]

        if plus > 0 and plus > minus:
            dm_plus[i] = plus

        if minus > 0 and minus > plus:
            dm_minus[i] = minus

    di_plus = np.asarray(SMMA(dm_plus, period)) * 100 / atr
    di_minus = np.asarray(SMMA(dm_minus, period)) * 100 / atr

    preprocessed_adx = np.abs(np.nan_to_num(np.divide(di_plus - di_minus, di_plus + di_minus)))
    adx = 100 * np.asarray(SMMA(preprocessed_adx, period))

    return (adx, di_plus, di_minus)
