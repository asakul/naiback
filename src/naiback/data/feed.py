
class Bar:

    def __init__(self, open_, high, low, close, volume, timestamp):
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.timestamp = timestamp

class Feed:
    """
    Interface for data source
    """

    def __init__(self):
        pass
