
from naiback.data.feed import Feed, Bar
import csv
import datetime
import itertools

class GenericCSVFeed(Feed):

    def __init__(self, fp):
        self.bars = []
        self.ticker_ = None
        reader = csv.reader(fp, delimiter=',')
        next(reader)
        for row in reader:
            try:
                self.ticker_ = row[0]
                open_ = float(row[4])
                high = float(row[5])
                low = float(row[6])
                close = float(row[7])
                volume = int(row[8])
                date = row[2]
                time = row[3]
                dt = datetime.datetime.strptime(date + "_" + time, "%Y%m%d_%H%M%S")
                self.bars.append(Bar(open_, high, low, close, volume, dt))
            except IndexError:
                pass

    def type(self):
        return 'bars'

    def items(self):
        return self.bars

    def ticker(self):
        return self.ticker_
