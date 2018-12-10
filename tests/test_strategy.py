
import pytest
import datetime
import io

from naiback.data.feeds.genericcsvfeed import GenericCSVFeed
from naiback.strategy.strategy import Strategy


@pytest.fixture
def feed():
    data = '''<TICKER>,<PER>,<DATE>,<TIME>,<OPEN>,<HIGH>,<LOW>,<CLOSE>,<VOL>
MICEX,D,20100111,000000,1411.3700000,1456.7600000,1411.3700000,1444.7800000,51634239250
MICEX,D,20100112,000000,1444.7800000,1445.6400000,1424.8700000,1427.6700000,38343314792
MICEX,D,20100113,000000,1417.8000000,1444.7700000,1412.9300000,1435.0100000,42183285247
MICEX,D,20100114,000000,1439.5500000,1456.2700000,1439.5500000,1455.6500000,44372479120
'''
    f = GenericCSVFeed(io.StringIO(data))
    return f

class BuyAndSell(Strategy):

    def __init__(self, buy_bar, sell_bar, ticker='MICEX'):
        super().__init__()
        self.buy_bar = buy_bar
        self.sell_bar = sell_bar
        self.ticker = ticker

    def execute(self):
        pos = self.buy_at_open(self.buy_bar, self.ticker)
        self.exit_at_close(self.sell_bar, pos)

class BuyAndSellLimit(Strategy):

    def __init__(self, buy_bar, buy_price, sell_bar, sell_price, ticker='MICEX'):
        super().__init__()
        self.buy_bar = buy_bar
        self.buy_price = buy_price
        self.sell_bar = sell_bar
        self.sell_price = sell_price
        self.ticker = ticker

    def execute(self):
        pos = self.buy_at_limit(self.buy_bar, self.buy_price, self.ticker)
        self.exit_at_limit(self.sell_bar, self.sell_price, pos)

class BuyOpenAndSellStop(Strategy):

    def __init__(self, buy_bar, sell_bar, sell_price, ticker='MICEX'):
        super().__init__()
        self.buy_bar = buy_bar
        self.sell_bar = sell_bar
        self.sell_price = sell_price
        self.ticker = ticker

    def execute(self):
        pos = self.buy_at_open(self.buy_bar, self.ticker)
        self.exit_at_stop(self.sell_bar, self.sell_price, pos)

class ShortAndCover(Strategy):

    def __init__(self, short_bar, cover_bar, ticker='MICEX'):
        super().__init__()
        self.short_bar = short_bar
        self.cover_bar = cover_bar
        self.ticker = ticker

    def execute(self):
        pos = self.short_at_open(self.short_bar, self.ticker)
        self.exit_at_close(self.cover_bar, pos)

class ShortAndCoverLimit(Strategy):

    def __init__(self, short_bar, short_price, cover_bar, cover_price, ticker='MICEX'):
        super().__init__()
        self.short_bar = short_bar
        self.short_price = short_price
        self.cover_bar = cover_bar
        self.cover_price = cover_price
        self.ticker = ticker

    def execute(self):
        pos = self.short_at_limit(self.short_bar, self.short_price, self.ticker)
        self.exit_at_limit(self.cover_bar, self.cover_price, pos)

class ShortOpenAndCoverStop(Strategy):

    def __init__(self, short_bar, cover_bar, cover_price, ticker='MICEX'):
        super().__init__()
        self.short_bar = short_bar
        self.cover_bar = cover_bar
        self.cover_price = cover_price
        self.ticker = ticker

    def execute(self):
        pos = self.short_at_open(self.short_bar, self.ticker)
        self.exit_at_stop(self.cover_bar, self.cover_price, pos)

def test_buy_and_sell_1(feed):
    s = BuyAndSell(0, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1444.78 - 1411.37))

def test_buy_and_sell_2(feed):
    s = BuyAndSell(0, 1)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1427.67 - 1411.37))

def test_buy_and_sell_3(feed):
    s = BuyAndSell(1, 2)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1435.01 - 1444.78))

def test_buy_and_sell_1_index(feed):
    s = BuyAndSell(0, 0, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1444.78 - 1411.37))

def test_buy_and_sell_limit_1(feed):
    s = BuyAndSellLimit(0, 1412, 1, 1445)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1445 - 1411.37))
    assert(not s.last_position_is_active())

def test_buy_and_sell_limit_2(feed):
    s = BuyAndSellLimit(1, 1430, 2, 1440)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1440 - 1430))
    assert(not s.last_position_is_active())

def test_buy_and_sell_limit_3(feed):
    s = BuyAndSellLimit(1, 1450, 2, 1410)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1417.80 - 1444.78))
    assert(not s.last_position_is_active())

def test_buy_and_sell_limit_1_index(feed):
    s = BuyAndSellLimit(0, 1412, 1, 1445, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1445 - 1411.37))
    assert(not s.last_position_is_active())

def test_buy_and_sell_stop_1(feed):
    s = BuyOpenAndSellStop(0, 1, 1430)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1430 - 1411.37))
    assert(not s.last_position_is_active())

def test_buy_and_sell_stop_2(feed):
    s = BuyOpenAndSellStop(0, 1, 1450)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1444.78 - 1411.37))
    assert(not s.last_position_is_active())

def test_buy_and_sell_stop_1_index(feed):
    s = BuyOpenAndSellStop(0, 1, 1430, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1430 - 1411.37))
    assert(not s.last_position_is_active())

def test_short_and_cover_1(feed):
    s = ShortAndCover(0, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1411.37 - 1444.78))

def test_short_and_cover_2(feed):
    s = ShortAndCover(0, 1)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1411.37 - 1427.67))

def test_short_and_cover_1_index(feed):
    s = ShortAndCover(0, 0, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1411.37 - 1444.78))

def test_short_and_cover_limit_1(feed):
    s = ShortAndCoverLimit(0, 1450, 1, 1430)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()

    assert(ending_cash == (initial_cash + 1450 - 1430))
    assert(not s.last_position_is_active())

def test_short_and_cover_limit_2(feed):
    s = ShortAndCoverLimit(0, 1410, 1, 1430)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()

    assert(ending_cash == (initial_cash + 1411.37 - 1430))
    assert(not s.last_position_is_active())

def test_short_and_cover_limit_3(feed):
    s = ShortAndCoverLimit(0, 1430, 1, 1450)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()

    assert(ending_cash == (initial_cash + 1430 - 1444.78))
    assert(not s.last_position_is_active())

def test_short_and_cover_limit_1_index(feed):
    s = ShortAndCoverLimit(0, 1450, 1, 1430, 0)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()

    assert(ending_cash == (initial_cash + 1450 - 1430))
    assert(not s.last_position_is_active())

def test_short_and_cover_stop_1(feed):
    s = ShortOpenAndCoverStop(0, 1, 1445)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1411.37 - 1445))
    assert(not s.last_position_is_active())

def test_short_and_cover_stop_2(feed):
    s = ShortOpenAndCoverStop(0, 1, 1440)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1411.37 - 1444.78))
    assert(not s.last_position_is_active())

def test_short_and_cover_stop_1_index(feed):
    s = ShortOpenAndCoverStop(0, 1, 1445)
    s.add_feed(feed)

    initial_cash = s.broker.cash()

    s.run()

    ending_cash = s.broker.cash()
    assert(ending_cash == (initial_cash + 1411.37 - 1445))
    assert(not s.last_position_is_active())

