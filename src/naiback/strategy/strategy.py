from abc import abstractmethod
from naiback.broker.position import Position
from naiback.broker.broker import Broker
from naiback.data.bars import Bars
from naiback.analyzers.statsanalyzer import StatsAnalyzer
from naiback.analyzers.tradeslistanalyzer import TradesListAnalyzer
from naiback.analyzers.equityanalyzer import EquityAnalyzer
from naiback.exceptions import NaibackException

import math

class Strategy:
    """
    """

    def __init__(self):
        self.feeds = []
        self.all_bars = []
        self.broker = Broker()
        self.bars = None
        self.trade_size = 1
        self.analyzers = { 'stats' : StatsAnalyzer(self),
                           'tradeslist' : TradesListAnalyzer(self),
                           'equity' : EquityAnalyzer(self) }

    def get_analyzer(self, analyzer_id):
        return self.analyzers[analyzer_id]

    def add_feed(self, feed):
        """
        Adds feed to feeds list.
        """
        self.feeds.append(feed)

    def set_trade_size(self, size):
        self.trade_size = math.floor(size)

    @abstractmethod
    def execute(self):
        """
        Will be called by 'run'
        """
        pass

    def run(self, from_time=None, to_time=None):
        """
        By default, just calls execute.
        """
        self._prepare_bars(from_time, to_time)
        if len(self.all_bars) > 0:
            self.bars = self.all_bars[0]
        self.execute()

    def set_current_ticker(self, ticker):
        self.bars = self._get_bars(ticker)

    def _prepare_bars(self, from_time, to_time):
        if len(self.feeds) == 0:
            raise NaibackException('No feeds added to strategy')

        self.all_bars.clear()
        for feed in self.feeds:
            if from_time is None or to_time is None:
                self.all_bars.append(Bars.from_feed(feed))
            else:
                self.all_bars.append(Bars.from_feed_filter(feed, from_time, to_time))

        all_dates = list(sorted(self._combine_dates()))

        for bars in self.all_bars:
            self._synchronize_bars(bars, all_dates)
            bars.index = range(0, len(bars.close))

    def get_bars(self, ticker):
        return self._get_bars(ticker)

    def _get_bars(self, ticker):
        for bars in self.all_bars:
            if bars.ticker == ticker:
                return bars

        return None

    def last_position(self):
        return self.broker.last_position()

    def all_positions(self):
        return self.broker.all_positions()

    def last_position_is_active(self):
        return self.broker.last_position_is_active()

    def _synchronize_bars(self, bars, all_dates):
        bar_pos = 0
        open_ = 0
        high = 0
        low = 0
        close = 0
        volume = bars.volume[bar_pos]
        for dt in all_dates:
            if len(bars.timestamp) > bar_pos:
                print("new close: {} ({})".format(close, dt))
                    
                if bars.timestamp[bar_pos] > dt:
                    print("Inserting at {}: {}".format(dt, close))
                    bars.insert_bar(bar_pos, open_, high, low, close, volume, dt)
                else:
                    open_ = bars.open[bar_pos]
                    high = bars.high[bar_pos]
                    low = bars.low[bar_pos]
                    close = bars.close[bar_pos]
                    volume = bars.volume[bar_pos]
                    if bars.timestamp[bar_pos] > dt:
                        bars.insert_bar(bar_pos, open_, high, low, close, volume, dt)
                    print("new close: {} ({})".format(close, dt))
                    
            else:
                bars.insert_bar(bar_pos, open_, high, low, close, volume, dt)
                print("Inserting[2] at {}: {}".format(dt, close))
                    
            bar_pos += 1

    def _combine_dates(self):
        dates = set()
        for bars in self.all_bars:
            dates.update(bars.timestamp)

        return dates

    def buy_at_open(self, bar, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        return self.broker.add_position(ticker, bars.open[bar], self.trade_size, bar)

    def buy_at_limit(self, bar, price, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        if bars.low[bar] <= price:
            if bars.open[bar] > price:
                return self.broker.add_position(ticker, price, self.trade_size, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], self.trade_size, bar)
        else:
            return None

    def buy_at_stop(self, bar, price, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        if bars.high[bar] >= price:
            if bars.open[bar] < price:
                return self.broker.add_position(ticker, price, self.trade_size, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], self.trade_size, bar)
        else:
            return None

    def buy_at_close(self, bar, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        return self.broker.add_position(ticker, bars.close[bar], self.trade_size, bar)

    def short_at_open(self, bar, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        return self.broker.add_position(ticker, bars.open[bar], -self.trade_size, bar)

    def short_at_limit(self, bar, price, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        if bars.high[bar] >= price:
            if bars.open[bar] < price:
                return self.broker.add_position(ticker, price, -self.trade_size, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], -self.trade_size, bar)
        else:
            return None

    def short_at_stop(self, bar, price, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        if bars.low[bar] <= price:
            if bars.open[bar] > price:
                return self.broker.add_position(ticker, price, -self.trade_size, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], -self.trade_size, bar)
        else:
            return None

    def short_at_close(self, bar, ticker=None):
        if ticker is None:
            ticker = 0
        if isinstance(ticker, int):
            ticker = self.all_bars[ticker].ticker
        bars = self._get_bars(ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        return self.broker.add_position(ticker, bars.close[bar], -self.trade_size, bar)

    def exit_at_open(self, bar, pos):
        bars = self._get_bars(pos.ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        return self.broker.close_position(pos, bars.open[bar], bar)

    def exit_at_limit(self, bar, price, pos):
        bars = self._get_bars(pos.ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        if pos.is_long():
            if bars.high[bar] >= price:
                if bars.open[bar] < price:
                    return self.broker.close_position(pos, price, bar)
                else:
                    return self.broker.close_position(pos, bars.open[bar], bar)
            else:
                return False
        else:
            if bars.low[bar] <= price:
                if bars.open[bar] > price:
                    return self.broker.close_position(pos, price, bar)
                else:
                    return self.broker.close_position(pos, bars.open[bar], bar)
            else:
                return False

    def exit_at_stop(self, bar, price, pos):
        bars = self._get_bars(pos.ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        if pos.is_long():
            if bars.low[bar] <= price:
                if bars.open[bar] > price:
                    return self.broker.close_position(pos, price, bar)
                else:
                    return self.broker.close_position(pos, bars.open[bar], bar)
            else:
                return False
        else:
            if bars.high[bar] >= price:
                if bars.open[bar] < price:
                    return self.broker.close_position(pos, price, bar)
                else:
                    return self.broker.close_position(pos, bars.open[bar], bar)
            else:
                return False

    def exit_at_close(self, bar, pos):
        bars = self._get_bars(pos.ticker)
        self.broker.set_timestamp(bars.timestamp[bar])
        return self.broker.close_position(pos, bars.close[bar], bar)

