
from naiback.strategy import SingleAssetStrategy
from naiback.data.feeds import FinamCSVFeed
from naiback.indicators import SMA, RSI

class MyStrategy(SingleAssetStrategy):

    def __init__(self):
        super().__init__()

    def execute(self):
        exit_sma = SMA(self.bars.close, 22)
        sma = SMA(self.bars.close, 200)
        rsi = RSI(self.bars.close, 2)
        stop = 0
        for i in self.bars.index[200:]:
            if self.last_position_is_active():
                if not self.exit_at_stop(i, self.last_position(), stop):
                    if self.bars.close[i] < exit_sma[i]:
                        self.exit_at_close(i, self.last_position())
            else:
                if self.bars.close[i] > exit_sma[i] and self.bars.close[i] > sma[i] and rsi[i] < 20:
                    self.buy_at_open(i + 1)

if __name__ == "__main__":
    strategy = MyStrategy()
    strategy.add_feed(FinamCSVFeed('data/SBER_20100101_20161231_daily.csv'))
    strategy.run(from_time='2012-01-01', to_time='2016-12-31')
    print(strategy.get_analyzer('stats').generate_plain_text())
