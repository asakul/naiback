
from naiback.strategy import Strategy
from naiback.data.feeds import GenericCSVFeed
from naiback.indicators import EMA, RSI

class MyStrategy(Strategy):

    def __init__(self):
        super().__init__()

    def execute(self):
        self.set_current_ticker('SBER')
        rsi1 = RSI(self.bars.close, 2)
        self.set_current_ticker('GAZP')
        rsi2 = RSI(self.bars.close, 2)
        for i in self.bars.index[200:-1]:
            if self.last_position_is_active():
                if i - self.last_position().entry_bar() > 3:
                    for position in self.all_positions():
                        self.exit_at_close(i, position)
            else:
                if rsi1[i] < 20 and rsi2[i] > 80:
                    self.buy_at_open(i + 1, 'SBER')
                    self.short_at_open(i + 1, 'GAZP')

if __name__ == "__main__":
    strategy = MyStrategy()
    strategy.add_feed(GenericCSVFeed(open('data/SBER_20100101_20171231_daily.csv', 'r')))
    strategy.add_feed(GenericCSVFeed(open('data/GAZP_20100101_20171231_daily.csv', 'r')))
    strategy.run(from_time='2012-01-01', to_time='2017-12-31')
    print(strategy.get_analyzer('stats').generate_plain_text())
