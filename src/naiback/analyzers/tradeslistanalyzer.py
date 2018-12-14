
from .analyzer import Analyzer

class TradesListAnalyzer(Analyzer):

    def __init__(self, strategy):
        self.strategy = strategy

    def get_result(self):
        positions = self.strategy.broker.retired_positions()
        return [self.make_trade(pos) for pos in positions]

    def make_trade(self, pos):
        return { 'entry_price' : pos.entry_price(),
                 'exit_price' : pos.exit_price(),
                 'entry_time' : pos.entry_time(),
                 'exit_time' : pos.exit_time(),
                 'pnl' : pos.pnl(),
                 'is_long' : pos.is_long(),
                 'security' : pos.ticker }
