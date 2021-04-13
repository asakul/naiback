
from naiback.data.feed import Feed, Bar
import csv
import datetime
import itertools

class YahooCSVFeed(Feed):

    def __init__(self, fp):
        self.bars = []
        self.ticker_ = None
        reader = csv.reader(fp, delimiter=',')
        next(reader)
        for row in reader:
            try:
                self.ticker_ = row[0]
                open_ = float(row[1])
                high = float(row[2])
                low = float(row[3])
                close = float(row[4])
                volume = int(row[6])
                date = row[0]
                dt = datetime.datetime.strptime(date, "%Y-%m-%d")
                self.bars.append(Bar(open_, high, low, close, volume, dt))
            except IndexError:
                pass

    def type(self):
        return 'bars'

    def items(self):
        return self.bars

    def ticker(self):
        return self.ticker_
