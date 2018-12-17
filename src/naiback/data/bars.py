
from ..exceptions import NaibackException

import datetime
import numpy as np

def bar_number(timeframe, timestamp):
    return timestamp.timestamp() // timeframe

def timestamp_from_bar_number(timeframe, bar_number):
    return datetime.datetime.utcfromtimestamp(bar_number * timeframe)

class Bars:
    """
    Basic bar series structure
    """

    DAILY = 86400
    HOUR = 3600
    MINUTE = 60

    def __init__(self, ticker):
        self.ticker = ticker
        self.index = []
        self.open = []
        self.high = []
        self.low = []
        self.close = []
        self.volume = []
        self.timestamp = []

    def append_bar(self, open_, high, low, close, volume, timestamp):
        """
        Appends OHLCV data
        """
        self.index.append(len(self.open))
        self.open.append(open_)
        self.high.append(high)
        self.low.append(low)
        self.close.append(close)
        self.volume.append(volume)
        self.timestamp.append(timestamp)

    def insert_bar(self, index, open_, high, low, close, volume, timestamp):
        self.open.insert(index, open_)
        self.high.insert(index, high)
        self.low.insert(index, low)
        self.close.insert(index, close)
        self.volume.insert(index, volume)
        self.timestamp.insert(index, timestamp)

    @classmethod
    def from_feed(cls, feed):
        if feed.type() != 'bars':
            raise NaibackException('Invalid feed type: "{}", should be "bars"'.format(feed.type()))
        bars = Bars(feed.ticker())
        for bar in feed.items():
            bars.append_bar(bar.open, bar.high, bar.low, bar.close, bar.volume, bar.timestamp)
        return bars

    @classmethod
    def from_feed_filter(cls, feed, from_time, to_time):
        if feed.type() != 'bars':
            raise NaibackException('Invalid feed type: "{}", should be "bars"'.format(feed.type()))
        bars = Bars(feed.ticker())
        for bar in feed.items():
            if bar.timestamp >= from_time and bar.timestamp <= to_time:
                bars.append_bar(bar.open, bar.high, bar.low, bar.close, bar.volume, bar.timestamp)
        return bars

    def upscale(self, new_timeframe):
        assert(len(self.open) == len(self.high))
        assert(len(self.open) == len(self.low))
        assert(len(self.open) == len(self.close))
        assert(len(self.open) == len(self.volume))
        assert(len(self.open) == len(self.timestamp))
        assert(len(self.open) > 0)

        new_open = []
        new_high = []
        new_low = []
        new_close = []
        new_volume = []
        new_timestamp = []

        current_bar = [self.open[0], self.high[0], self.low[0], self.close[0], self.volume[0]]
        current_bar_number = bar_number(new_timeframe, self.timestamp[0])
        for i in range(1, len(self.open)):
            next_bar_number = bar_number(new_timeframe, self.timestamp[i])
            if next_bar_number == current_bar_number:
                current_bar[1] = max(current_bar[1], self.high[i])
                current_bar[2] = min(current_bar[2], self.low[i])
                current_bar[3] = self.close[i]
                current_bar[4] += self.volume[i]
            else:
                new_open.append(current_bar[0])
                new_high.append(current_bar[1])
                new_low.append(current_bar[2])
                new_close.append(current_bar[3])
                new_volume.append(current_bar[4])
                new_timestamp.append(timestamp_from_bar_number(new_timeframe, current_bar_number))
                current_bar = [self.open[i], self.high[i], self.low[i], self.close[i], self.volume[i]]
                current_bar_number = next_bar_number

        new_open.append(current_bar[0])
        new_high.append(current_bar[1])
        new_low.append(current_bar[2])
        new_close.append(current_bar[3])
        new_volume.append(current_bar[4])
        new_timestamp.append(timestamp_from_bar_number(new_timeframe, current_bar_number))

        b = Bars(self.ticker)
        b.index = range(0, len(new_open))
        b.open = new_open
        b.high = new_high
        b.low = new_low
        b.close = new_close
        b.volume = new_volume
        b.timestamp = new_timestamp
        return b

    def synchronize_indicator(self, indicator, other):
        ix1 = 0
        ix2 = 0

        new_indicator = []

        for ix2 in range(0, len(other.open)):
            if ix1 > 0:
                if ix1 < len(indicator) - 1:
                    if other.timestamp[ix2] < self.timestamp[ix1 + 1]:
                        new_indicator.append(indicator[ix1 - 1])
                    else:
                        ix1 += 1
                        new_indicator.append(indicator[ix1 - 1])
                else:
                    new_indicator.append(0)
            else:
                if other.timestamp[ix2] >= self.timestamp[ix1 + 1]:
                    ix1 += 1
                new_indicator.append(0)
        
        return np.array(new_indicator)
                
    def synchronize_to(self, other):
        ix1 = 0
        ix2 = 0

        new_open = []
        new_high = []
        new_low = []
        new_close = []
        new_volume = []
        new_timestamp = []

        for i in range(0, len(other.open)):
            if ix1 < len(self.open) - 1:
                if other.timestamp[ix2] < self.timestamp[ix1 + 1]:
                    new_open.append(self.open[ix1 + 1])
                    new_high.append(self.high[ix1 + 1])
                    new_low.append(self.low[ix1 + 1])
                    new_close.append(self.close[ix1 + 1])
                    new_volume.append(0)
                    new_timestamp.append(other.timestamp[ix2])
                else:
                    if ix1 < len(self.open) - 2:
                        ix1 += 1
                        new_open.append(self.open[ix1 + 1])
                        new_high.append(self.high[ix1 + 1])
                        new_low.append(self.low[ix1 + 1])
                        new_close.append(self.close[ix1 + 1])
                        new_volume.append(0)
                        new_timestamp.append(other.timestamp[ix2])
                    else:
                        new_open.append(self.open[ix1])
                        new_high.append(self.high[ix1])
                        new_low.append(self.low[ix1])
                        new_close.append(self.close[ix1])
                        new_volume.append(0)
                        new_timestamp.append(other.timestamp[ix2])
            else:
                new_open.append(self.open[ix1])
                new_high.append(self.high[ix1])
                new_low.append(self.low[ix1])
                new_close.append(self.close[ix1])
                new_volume.append(0)
                new_timestamp.append(other.timestamp[ix2])
            ix2 += 1

        self.index = range(0, len(new_open))
        self.open = new_open
        self.high = new_high
        self.low = new_low
        self.close = new_close
        self.volume = new_volume
        self.timestamp = new_timestamp

