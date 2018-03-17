
from naiback.data.feed import Feed, Bar
import csv
import datetime
import itertools

class GenericCSVFeed(Feed):

    def __init__(self, fp):
        self.bars = []
        reader = csv.reader(fp, delimiter=',')
        next(reader)
        next(reader)
        for row in reader:
            try:
                open_ = row[4]
                high = row[5]
                low = row[6]
                close = row[7]
                volume = row[8]
                date = row[2]
                time = row[3]
                dt = datetime.datetime.strptime(date + "_" + time, "%Y%m%d_%H%M%S")
                self.bars.append(Bar(open_, high, low, close, volume, dt))
            except IndexError:
                pass

    def items(self):
        return self.bars
