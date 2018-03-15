
from naiback.strategy import Strategy
from naiback.data.feeds import FinamCSVFeed
from naiback.indicators import SMA, RSI

class MyStrategy(BarStrategy):

    def __init__(self):
        super().__init__()

    def execute(self):
        self.set_context('FOO')
        rsi1 = RSI(self.bars.close, 2)
        self.set_context('BAR')
        rsi2 = RSI(self.bars.close, 2)
        for i in self.bars.index[200:]:
            if self.last_position_is_active():
                if i - self.last_position().entry_bar > 3:
                    for position in self.all_positions():
                        position.exit_at_close(i)
            else:
                if rsi1[i] < 20 and rsi2[i] > 80:
                    self.buy_at_open(i + 1, 'FOO')
                    self.short_at_open(i + 1, 'BAR')

if __name__ == "__main__":
    strategy = MyStrategy()
    strategy.add_feed(FinamCSVFeed('data/SBER_20100101_20161231_daily.csv'))
    strategy.run(from_time='2012-01-01', to_time='2016-12-31')
    print(strategy.get_analyzer('stats').generate_plain_text())
