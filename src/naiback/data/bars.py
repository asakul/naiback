
from ..exceptions import NaibackException

class Bars:
    """
    Basic bar series structure
    """

    def __init__(self):
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

    @classmethod
    def from_feed(feed):
        if feed.type() != 'bars':
            raise NaibackException('Invalid feed type: "{}", should be "bars"'.format(feed.type()))
        bars = Bars()
        for bar in feed.items():
            bars.append_bar(bar.open, bar.high, bar.low, bar.close, bar.volume, bar.timestamp)
        return bars
