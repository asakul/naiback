
import pytest
import datetime

from naiback.data.bars import Bars

def test_bar_append():
    bars = Bars('FOO')
    bars.append_bar(10, 20, 5, 11, 100, datetime.datetime(2017, 1, 1))

    assert bars.open[0] == 10
    assert bars.high[0] == 20
    assert bars.low[0] == 5
    assert bars.close[0] == 11
    assert bars.volume[0] == 100
    assert bars.timestamp[0] == datetime.datetime(2017, 1, 1)
