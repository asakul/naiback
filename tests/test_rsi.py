
import pytest
import datetime

from naiback.indicators.rsi import RSI

def test_rsi_1():
    data = [252.12, 253.97, 253.73, 255.06, 255.14, 256.71, 256.15, 258.51, 255.24, 252.63, 253.82, 254.16, 253.99, 254.47,
            255.93, 255, 253.21, 251.03]
    rsi = RSI(data, 3)

    assert(abs(rsi[-1] - 14.7) < 0.1)
    assert(len(rsi) == len(data))

