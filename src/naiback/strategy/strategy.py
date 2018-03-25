from abc import abstractmethod
from naiback.broker.position import Position
from naiback.broker.broker import Broker
from naiback.data.bars import Bars

class Strategy:
    """
    """

    def __init__(self):
        self.feeds = []
        self.all_bars = []
        self.broker = Broker()
        self.bars = None

    def add_feed(self, feed):
        """
        Adds feed to feeds list.
        """
        self.feeds.append(feed)

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
        self._prepare_bars()
        self.execute()

    def set_current_ticker(self, ticker):
        self.bars = self._get_bars(ticker)

    def _prepare_bars(self):
        if len(self.feeds) == 0:
            raise NaibackException('No feeds added to strategy')

        self.all_bars.clear()
        for feed in self.feeds:
            self.all_bars.append(Bars.from_feed(feed))

        all_dates = list(sorted(self._combine_dates()))

        for bars in self.all_bars:
            self._synchronize_bars(bars, all_dates)

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
        for dt in all_dates:
            if bars.timestamp[bar_pos] > dt:
                open_ = bars.open[bar_pos]
                high = bars.high[bar_pos]
                low = bars.low[bar_pos]
                close = bars.close[bar_pos]
                volume = bars.volume[bar_pos]

                bars.insert_bar(bar_pos, open_, high, low, close, volume, dt)

    def _combine_dates(self):
        dates = set()
        for bars in self.all_bars:
            dates.update(bars.timestamp)

        return dates

    def buy_at_open(self, bar, ticker):
        bars = self._get_bars(ticker)
        return self.broker.add_position(ticker, bars.open[bar], 1, bar)

    def buy_at_limit(self, bar, price, ticker):
        bars = self._get_bars(ticker)
        if bars.low[bar] <= price:
            if bars.open[bar] > price:
                return self.broker.add_position(ticker, price, 1, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], 1, bar)
        else:
            return None

    def buy_at_stop(self, bar, price, ticker):
        bars = self._get_bars(ticker)
        if bars.high[bar] >= price:
            if bars.open[bar] < price:
                return self.broker.add_position(ticker, price, 1, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], 1, bar)
        else:
            return None

    def buy_at_close(self, bar, ticker):
        bars = self._get_bars(ticker)
        return self.broker.add_position(ticker, bars.close[bar], 1, bar)

    def short_at_open(self, bar, ticker):
        bars = self._get_bars(ticker)
        return self.broker.add_position(ticker, bars.open[bar], -1, bar)

    def short_at_limit(self, bar, price, ticker):
        bars = self._get_bars(ticker)
        if bars.high[bar] >= price:
            if bars.open[bar] < price:
                return self.broker.add_position(ticker, price, -1, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], -1, bar)
        else:
            return None

    def short_at_stop(self, bar, price, ticker):
        bars = self._get_bars(ticker)
        if bars.low[bar] <= price:
            if bars.open[bar] > price:
                return self.broker.add_position(ticker, price, -1, bar)
            else:
                return self.broker.add_position(ticker, bars.open[bar], -1, bar)
        else:
            return None

    def short_at_close(self, bar, ticker):
        bars = self._get_bars(ticker)
        return self.broker.add_position(ticker, bars.close[bar], -1, bar)

    def exit_at_open(self, bar, pos):
        bars = self._get_bars(pos.ticker)
        return self.broker.close_position(pos, bars.open[bar], bar)

    def exit_at_limit(self, bar, price, pos):
        bars = self._get_bars(pos.ticker)
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
        return self.broker.close_position(pos, bars.close[bar], bar)

