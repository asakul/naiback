
import pytest
import datetime

from naiback.indicators.ema import EMA

def test_ema_1():
    data = [1, 1, 1]
    ema = EMA(data, 1)

    assert(ema == [None, 1, 1])

def test_ema_2():
    data = [1, 3, 5]
    ema = EMA(data, 3)

    assert(ema == [None, 2, 3.5])

def test_ema_3():
    data = [252.12, 253.97, 253.73, 255.06, 255.14, 256.71, 256.15, 258.51, 255.24, 252.63]
    ema = EMA(data, 3)

    assert(abs(ema[-1] - 254.43) < 0.01)
    assert(len(ema) == len(data))

